from typing import Union, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Table
    from models import Selection

class Selection:
    def __init__(self, parent: Union["Table", "Selection"], condition: Callable, entries: list):
        self.parent = parent
        self.condition = condition
        self.entries = entries
    
    def set(self, key, value):
        if not callable(value):
            val = lambda entry: value
        else:
            val = value
        for entry in self.entries:
            entry[key] = val(entry)

    def get(self, key):
        for entry in self.entries:
            entry[key]

    def remove(self, key):
        for entry in self.entries:
            del entry[key]

    def where(self, condition) -> "Selection":
        if not callable(condition):
            cond = lambda entry: eval(condition, {}, {"_table": self, "_entry": entry, "uuid": entry.uuid, **entry.data})
        else:
            cond = condition
        final = lambda entry: self.condition(entry) and cond(entry)
        return self.parent.where(final)

    def delete(self):
        for entry in self.entries:
            del self.parent[entry.uuid]

    __setitem__ = set
    __getitem__ = get
    __delitem__ = remove
    # __del__ = delete      !!! Results in everything getting deleted.

    def others(self):
        return self.parent.where(lambda e: not self.condition(e))

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    def __repr__(self):
        return f"<psv.Selection entries={len(self.entries)}>"