from .table import Table
import json

def encode(tbl: Table):
    txt = ""
    for entry in tbl.entries:
        entryjson = json.dumps(entry.data)
        txt += f"{entry.uuid} {entryjson}\n"
    return txt
