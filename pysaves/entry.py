from .utils import create_uuid

class Entry:
    def __init__(self, uuid: str, data: dict):
        if "uuid" in data:
            raise KeyError("No Key can be named uuid.")
        self.uuid = uuid
        self.data = data

    def __getitem__(self, key):
        if key == "uuid":
            return self.uuid
        if key in self.data:
            return self.data[key]
        return None

    def __setitem__(self, key, value):
        if key == "uuid":
            raise KeyError("uuid cannot be changed this way.")
        self.data[key] = value

    def __delitem__(self, key):
        if key == "uuid":
            raise KeyError("uuid cannot be deleted.")
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"<psv.Entry uuid={self.uuid} length={len(self.data)}>"

    @staticmethod
    def new(data: dict):
        return Entry(create_uuid(), data)

class NullEntry(Entry):
    def __init__(self, uuid: str):
        self.uuid = uuid

    def __getitem__(self, key):
        if key == "uuid":
            return self.uuid
        return None

    def __setitem__(self, key, value):
        if key == "uuid":
            raise KeyError("uuid cannot be changed this way.")

    def __len__(self):
        return 0

    def __repr__(self):
        return f"<psv.Entry uuid={self.uuid} length=0>"
