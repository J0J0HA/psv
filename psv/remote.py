from typing import Optional
from requests import get
from .decoder import decode
from .exceptions import InvalidConnectionError

class Status:
    success = "Success"
    result = "Result"
    failed = "Error"
    broken = "Unknown"

class Result:
    def __init__(self, status, value) -> None:
        self.status = status
        self.value = value

def request(host: str, port: int, passwd: str, action: str, info: Optional[list] = None):
    try:
        path = f"{host}:{port}/{action}"
        if info:
            path += "/" + "/".join(info)
        result = get(path, {"pass": passwd})
        response = result.text
        if result.text.startswith("[S] "):
            return Result(Status.success, response.removeprefix("[S]"))
        if result.text.startswith("[F] "):
            return Result(Status.failed, response.removeprefix("[F]"))
        if result.text.startswith("[R] "):
            return Result(Status.result, response.removeprefix("[R]"))
        return Result(Status.broken, response)
    finally:
        return Result(Status.broken, "No result recived.")

class ConnectTable:
    def __init__(self, passwd: str, host: str = "0.0.0.0", port: int = 4435) -> None:
        self.host = host
        self.port = port
        self.passwd = passwd
    
    def list(self):
        response = request(self.host, self.port, self.passwd, "get")
        if response.status != Status.result:
            raise InvalidConnectionError(f"Response was of unexcpected type {response.status}! Response was: {response.value}")
        return decode(response.value, self)
    
    # HERE STOPPED
        