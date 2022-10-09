from .table import Table, Entry
import json

def decode(txt: str):
    tbl = Table()
    for line in txt.split("\n"):
        if line.strip() == "" or line.startswith(":"):
            continue
        uuid, jsonstr = tuple(line.split(" ", 1))
        tbl.append(Entry(uuid, json.loads(jsonstr)))
    return tbl
