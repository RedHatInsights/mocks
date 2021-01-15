from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


user_db = TinyDB(storage=MemoryStorage)
request_db = TinyDB(storage=MemoryStorage)
org_db = TinyDB(storage=MemoryStorage)
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


def upsert_org(org_id, ebs_account, external_id):
    """
    Used by accounts_mgmt to track the orgs that have been requested/generated on-the-fly.
    :param org_id: The unique identifier of the fake org.
    :param ebs_account: The EBS account ID.
    :param external_id: The external id.
    """
    return org_db.upsert(
        {"org_id": org_id, "ebs_account": ebs_account, "external_id": external_id},
        query.org_id == org_id,
    )


def get_org(org_id):
    return org_db.get(query.org_id == org_id)
