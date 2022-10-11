from typing import Any
from .table import Table, Entry
import json

def encode(tbl: Table) -> str:
    rst = []
    for etr in tbl.entries:
        enc = encode_etr(etr)
        rst.append(enc)
    return "\n".join(rst)

def encode_etr(etr: Entry) -> str:
    rst = []
    for key, val in etr.data.items():
        eckey = encode_elm(key)
        ecval = encode_elm(val)
        rst.append(eckey + ":" + ecval)
    return etr.uuid + " " + ";".join(rst)

def encode_elm(elm: Any) -> str:
    cls = encode_class(elm)
    txt = encode_str(cls, elm)
    return f"{cls}|{txt}"

def encode_str(cls: str, elm: Any):
    rtxt = ""
    if cls == "str":
        rtxt = clean_str(elm)
    if cls == "int":
        rtxt = clean_str(str(elm))
    if cls == "flt":
        rtxt = clean_str(str(elm))
    return rtxt

def clean_str(txt: str) -> str:
    txt = txt.replace("!", "!w!")
    txt = txt.replace(";", "!s!")
    txt = txt.replace("\n", "!n!")
    txt = txt.replace(":", "!d!")
    txt = txt.replace("|", "!h!")
    return txt

def encode_class(elm: Any) -> str:
    if isinstance(elm, str):
        return "str"
    if isinstance(elm, int):
        return "int"
    if isinstance(elm, float):
        return "flt"
    try:
        elms = str(elm)
    except:
        elms = "<?>"
    raise TypeError(elms + " is of type " + type(elm) + " which is no supported type.")