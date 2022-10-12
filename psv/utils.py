from uuid import uuid4 as create_uuid
import time


def keep_alive():
    while True:
        time.sleep(1) # KEEP ALIVE
