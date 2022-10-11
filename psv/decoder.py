from .exceptions import NoSuchClassError, TooMuchDataError
from typing import Any
from .table import Table, Entry
import json

def decode(txt: str):
    tbl = Table()
    for line in txt.split("\n"):
        if line.strip() == "" or line.startswith(":"):
            continue
        tbl.append(decode_etr(line))
    return tbl

def decode_etr(txt: str) -> Entry:
    data = txt.split(" ", 1)
    uuid = data[0]
    pairs = data[1].split(";")
    dat = {}
    if pairs and pairs[0]:
        for pair in pairs:
            key, val = decode_pair(pair)
            dat[key] = val
    return Entry(uuid, dat)

def decode_pair(txt: str) -> tuple:
    data = txt.split(":", 1)
    if len(data) > 2:
        raise TooMuchDataError("More than one key and one value is given: ", data)
    key = decode_elm(data[0])
    val = decode_elm(data[1])
    return key, val

def decode_elm(txt: str) -> Any:
    data = txt.split("|", 1)
    if len(data) > 2:
        raise TooMuchDataError("More than one class and one value is given: ", data)
    val = decode_str(clean_str(data[0]), clean_str(data[1]))
    return val

def decode_str(cls: str, val: str) -> Any:
    if cls == "int":
        return int(val)
    if cls == "flt":
        return float(val)
    if cls == "str":
        return val
    raise NoSuchClassError("No class defined for class string '" + cls + "'", val)

def clean_str(txt: str) -> str:
    txt = txt.replace("!s!", ";")
    txt = txt.replace("!n!", "\n")
    txt = txt.replace("!d!", ":")
    txt = txt.replace("!h!", "|")
    txt = txt.replace("!w!", "!")
    return txt
