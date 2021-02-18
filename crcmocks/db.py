from tinydb import Query
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


user_db = TinyDB(storage=MemoryStorage)
request_db = TinyDB(storage=MemoryStorage)
query = Query()


def all_users():
    return user_db.all()


def add_user(data):
    user_db.upsert(data, query.username == data["username"])


def all_requests():
    return request_db.all()


def add_request(data):
    request_db.insert(data)


def clear_requests():
    request_db.purge()
