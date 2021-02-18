import json
from base64 import b64decode

from crcmocks.db import query
from crcmocks.db import user_db


def get_user_rh_identity(identity_header):
    """
    Given an base64 encoded identity header, find a user.
    """
    # decode the identity header
    identity_header = json.loads(b64decode(identity_header.encode("ascii")).decode("ascii"))
    account_number = identity_header.get("identity", {}).get("account_number")
    username = identity_header.get("identity", {}).get("user", {}).get("username")

    # lookup the user in tinyDB, based on the identity
    return (
        user_db.search(
            (query.account_number.search(str(account_number))) | (query.username == username)
        ),
        username,
        account_number,
    )


def get_users():
    """
    Get all users in TinyDB.

    This is different from kc_helper.get_realm_users() in that it returns permission/entitlement
    information, which is not stored in keycloak.
    """
    return user_db.all()
