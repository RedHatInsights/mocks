from copy import deepcopy

from flask import jsonify
from flask import Blueprint
from flask import request

from crcmocks.util import get_user_rh_identity
from crcmocks.config import DEFAULT_PERMISSIONS


blueprint = Blueprint("rbac", __name__)

BASE_RBAC_RESPONSE = {
    "meta": {"count": None, "limit": None, "offset": 0},
    "links": {
        "first": "/api/rbac/v1/access/?application=&format=json&limit=1000&offset=0",
        "next": None,
        "previous": None,
        "last": "/api/rbac/v1/access/?application=&format=json&limit=1000&offset=0",
    },
    "data": [],
}


# TODO: support resource definitions?
@blueprint.route("/v1/access/", methods=["GET"])
def rbac_access():
    application = request.args.get("application")
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
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

    # get the user permissions
    if user[0].get("permissions"):
        permissions = user[0]["permissions"].split(",")
    else:
        permissions = DEFAULT_PERMISSIONS.copy()

    rbac_response = deepcopy(BASE_RBAC_RESPONSE)
    # set links
    rbac_response["links"]["first"] = (
        f"/api/rbac/v1/access/?application={application or ''}"
        f"&format=json&limit={limit}"
        f"&offset={offset}"
    )
    rbac_response["links"]["last"] = (
        f"/api/rbac/v1/access/?application={application or ''}"
        f"&format=json&limit={limit}"
        f"&offset={offset}"
    )

    limit_count = 0
    # TODO: implement 'real' pagination
    for i, perm in enumerate(permissions):
        if i >= offset:
            if application:
                if perm.split(":")[0] in application:
                    rbac_response["data"].append({"resourceDefinitions": [], "permission": perm})
                    limit_count += 1
            else:
                rbac_response["data"].append({"resourceDefinitions": [], "permission": perm})
                limit_count += 1
            if limit_count == limit:
                break
    # set meta
    rbac_response["meta"]["limit"] = limit
    rbac_response["meta"]["count"] = limit_count

    return jsonify(rbac_response)
