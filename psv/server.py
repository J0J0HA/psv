import json
from pickletools import read_unicodestringnl
from typing import IO, Union, Callable
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response, Request
from .encoder import encode_etr, encode_elm
from .decoder import decode_pair, decode_elm, clean_str as unclean_str
from .table import Table
from .exceptions import TooMuchDataError, NoSuchClassError
from psv.entry import NullEntry
from .utils import create_uuid
import os
from .files import write


def create_server(tbl: Table, tblf: Union[str, None] = None):
    if not os.path.isfile(".psvpass"):
        with open(".psvpass", "w") as f:
            passwd = str(create_uuid())
            f.write(passwd)
    else:
        with open(".psvpass", "r") as f:
            passwd = f.read()

    def app(env, start_response):
        request = Request(env)
        p = request.path.removeprefix("/").split("/")
        if (not "pass" in request.args) or (request.args.get("pass") != passwd):
            return Response('[F] Error 403: Invalid API Key!', 403, mimetype='text/plain')(env, start_response)
        action = p[0]
        if action == "set":
            entry = tbl[p[1]]
            if isinstance(entry, NullEntry):
                response = Response('[F] Error 404: No such UUID!', 404, mimetype='text/plain')
            else:
                try:
                    key, value = decode_pair("/".join(p[2:]))
                    entry.data[key] = value
                    response = Response('[S] Success 200: Entry got editied!', 200, mimetype='text/plain')
                except (IndexError, TooMuchDataError, NoSuchClassError) as e:
                    response = Response('[F] Error 400: Invalid input!', 400, mimetype='text/plain')
                    print("FAILED", e)
            if tblf:
                with open(tblf, "w") as tf:
                    write(tf, tbl)
        elif action == "del":
            entry = tbl[p[1]]
            if isinstance(entry, NullEntry):
                response = Response('[F] Error 404: No such UUID!', 404, mimetype='text/plain')
            else:
                if len(p) > 2:
                    try:
                        key = decode_elm("/".join(p[2:]))
                        del entry.data[key]
                        response = Response('[S] Success 200: Entry got editied!', 200, mimetype='text/plain')
                    except (IndexError, TooMuchDataError, NoSuchClassError) as e:
                        response = Response('[F] Error 400: Invalid input!', 400, mimetype='text/plain')
                        print("FAILED", e)
                else:
                    try:
                        tbl.remove(entry.uuid)
                        response = Response('[S] Success 200: Entry got deleted!', 200, mimetype='text/plain')
                    except (IndexError, TooMuchDataError, NoSuchClassError) as e:
                        response = Response('[F] Error 400: Invalid input!', 400, mimetype='text/plain')
                        print("FAILED", e)
            if tblf:
                with open(tblf, "w") as tf:
                    write(tf, tbl)
        elif action == "get":
            if len(p) == 1:
                uuids = []
                for entry in tbl:
                    uuids.append(entry.uuid)
                response = Response("[R] " + ";".join(uuids), 200, mimetype='text/plain')
            else:
                entry = tbl[p[1]]
                if isinstance(entry, NullEntry):
                    response = Response('[F] Error 404: No such UUID!', 404, mimetype='text/plain')
                else:
                    if len(p) > 2:
                        try:
                            key = decode_elm("/".join(p[2:]))
                            response = Response("[R] " + encode_elm(entry.data[key]), 200, mimetype='text/plain')
                        except (IndexError, TooMuchDataError, NoSuchClassError) as e:
                            response = Response('[F] Error 400: Invalid input!', 400, mimetype='text/plain')
                            print("FAILED", e)
                    else:
                        try:
                            response = Response("[R] " + encode_etr(entry).split(" ", 1)[1], 200, mimetype='text/plain')
                        except (IndexError, TooMuchDataError, NoSuchClassError) as e:
                            response = Response('[F] Error 400: Invalid input!', 400, mimetype='text/plain')
                            print("FAILED", e)
        else:
            response = Response('[F] Error 404: No such API-Path!', 404, mimetype='text/plain')
        return response(env, start_response)

    def run(host: str, port: int):
        run_simple(host, port, app)

    return app, run

def share_table(tbl: Table, host: str = "0.0.0.0", port: int = 4435, autosave: Union[IO, None] = None):
    return create_server(tbl, autosave)[1](host, port)
