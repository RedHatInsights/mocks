import json
from base64 import b64decode

from crcmocks.db import User
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
            (User.account_number.search(str(account_number))) | (User.username == username)
        ),
        username,
        account_number,
    )
