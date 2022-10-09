from typing import TextIO
from .encoder import encode
from .decoder import decode
from .table import Table

def write(file: TextIO, table: Table):
    file.write(encode(table))

def load(file: TextIO):
    return decode(file.read())
