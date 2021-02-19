from flask import Blueprint
from flask import jsonify
from flask import request

from crcmocks.config import DEFAULT_SERVICES
from crcmocks.util import get_user_rh_identity


blueprint = Blueprint("entitlements", __name__)


# TODO: support is_trial?
@blueprint.route("/v1/services")
def services():
    # get the identity header
    identity_header = request.headers.get("X-Rh-Identity")

    if identity_header is None:
        return "No identity header present in request\n", 401

    # get the user
    user, username, account_number = get_user_rh_identity(identity_header)

    if not user:
        return (
            f"No user found in TinyDB with username:"
            f" {username} or account_number: {account_number}\n",
            404,
        )
    if len(user) > 1:
        return (
            f"Multiple users found with:" f" {username} or account_number: {account_number}\n",
            406,
        )

    # finally get the entitlements of the user
    if user[0].get("entitlements"):
        entitled_services = user[0]["entitlements"].split(",")
    else:
        entitled_services = DEFAULT_SERVICES.copy()

    entitlements = {}
    for svc in DEFAULT_SERVICES:
        entitlements[svc] = {"is_entitled": svc in entitled_services, "is_trial": False}
    return jsonify(entitlements), 200
