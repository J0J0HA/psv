from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Table

class Selection:
    def __init__(self, table: "Table", condition: Callable, entries: list):
        self.table = table
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

    def where(self, condition):
        if not callable(condition):
            cond = lambda entry: eval(condition, {}, {"_table": self, "_entry": entry, "uuid": entry.uuid, **entry.data})
        else:
            cond = condition
        final = lambda entry: self.condition(entry) and cond(entry)
        return self.table.where(final)

    def delete(self):
        for entry in self.entries:
            del self.table[entry.uuid]

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        raise NotImplementedError

    def __repr__(self):
        return f"<psv.Selection length={len(self.entries)}>"