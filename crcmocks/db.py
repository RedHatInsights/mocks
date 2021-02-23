import logging
import threading

from tinydb import Query
from tinydb import TinyDB

log = logging.getLogger(__name__)

user_db = TinyDB("/opt/tinydb/data/user_db.json")
request_db = TinyDB("/opt/tinydb/data/request_db.json")
User = Query()

user_db_lock = threading.RLock()
request_db_lock = threading.RLock()


def all_users():
    return user_db.all()


def add_user(data, skip_if_exists=False):
    if skip_if_exists and user_db.search(User.username == data["username"]):
        log.info("skipping localdb update for existing user: %s", data["username"])
        return
    with user_db_lock:
        user_db.upsert(data, User.username == data["username"])
    log.info("added/updated user in localdb: %s", data["username"])


def clear_users():
    with user_db_lock:
        user_db.truncate()


def all_requests():
    return request_db.all()


def add_request(data):
    with request_db_lock:
        request_db.insert(data)


def clear_requests():
    with request_db_lock:
        request_db.truncate()
