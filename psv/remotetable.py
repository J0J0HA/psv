from typing import IO, Union
from psv.selection import Selection
from .remoteentry import RemoteEntry, RemoteNullEntry


class RemoteTable:
    def __init__(self, table: dict = None):
        if table:
            for uuid, data in table.items():
                self.entries.append(Entry(uuid, data))
    
    @property
    def entries() -> list:
        return 

    def get(self, uuid: str):
        for entry in self.entries:
            if entry.uuid == uuid:
                print("E", entry)
                return entry
        print("F")
        return NullEntry(uuid)

    def append(self, entry: Entry):
        self.entries.append(entry)

    def new_entry(self, data: dict):
        entry = Entry.new(data)
        self.append(entry)
        return entry.uuid

    def remove(self, uuid: str):
        for entry in range(len(self.entries)):
            if self.entries[entry].uuid == uuid:
                del self.entries[entry]
                return

    def others(self) -> Selection:
        return Selection(self, lambda e: False, [])

    def where(self, condition) -> Selection:
        if not callable(condition):
            cond = lambda entry: eval(condition, {}, {"_table": self, "_entry": entry, "uuid": entry.uuid, **entry.data})
        else:
            cond = condition
        return Selection(self, cond, list(filter(cond, self)))

    __getitem__ = get
    __delitem__ = remove
    
    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    def __repr__(self):
        return f"<psv.Table entries={len(self.entries)}>"
