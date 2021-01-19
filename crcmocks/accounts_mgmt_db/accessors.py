from typing import List, Any

from tinydb import TinyDB, Query, where
from tinydb.storages import MemoryStorage

#
# This source file contains short-term persistent storage accessor functions needed by the
# accounts_mgmt mocks.
#

# org_db is a store for all of the details associated with an org
org_db = TinyDB(storage=MemoryStorage)

# account_db is just a mapping of which account id's belong to org ids.
account_db = TinyDB(storage=MemoryStorage)

query = Query()


def upsert_org(org_id, ebs_account, external_id):
    """
    Persists the org details that have been requested/generated on-the-fly.
    :param org_id: The unique identifier of the fake org.
    :param ebs_account: The fake EBS account ID.
    :param external_id: The fake external id.
    """
    return org_db.upsert(
        {"org_id": org_id, "ebs_account": ebs_account, "external_id": external_id},
        query.org_id == org_id,
    )


def get_org_by_id(org_id):
    """
    Get an org from the org db.
    """
    return org_db.get(query.org_id == org_id)


def get_all_orgs():
    return org_db.all()


def get_all_accounts():
    return account_db.all()


def get_account_by_id(account_id):
    """
    Get all tuples where the account id matches.
    :param account_id: The unique ID of the account (NOT EBS account id)
    """
    return account_db.search(where("account_id") == account_id)
    # return account_db.get(query.account_id == account_id)


def get_accounts_for_org(org_id) -> List[Any]:
    """
    Get the list of account IDs associated with an org ID.
    """
    return account_db.get(query.org_id == org_id)


def insert_account_mapping(account_id, org_id):
    """
    Associates an account_id with an organization id.
    """
    result = get_org_by_id(org_id)
    if not result:
        raise ValueError()
    account_db.insert({"org_id": org_id, "account_id": account_id})
