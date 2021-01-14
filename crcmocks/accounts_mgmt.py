import uuid
from copy import deepcopy

from flask import jsonify
from flask import Blueprint
from flask import request

# Mocks of some basic accounts_mgmt API endpoints needed for testing uhc-auth-proxy
# API ref: https://api.openshift.com/?urls.primaryName=Accounts%20management%20service

accounts_mgmt = Blueprint("accounts_mgmt", __name__)


class MissingAuth(Exception):
    pass


class BadBearerTokenValue(Exception):
    pass


def process_headers(headers: dict):
    """ Confirms the headers are structurally valid. """
    auth_header = headers.get("Authorization", None)
    if not auth_header:
        raise MissingAuth
    if not auth_header.startswith("Bearer "):
        raise BadBearerTokenValue
    return auth_header[7:]


@accounts_mgmt.route("/api/accounts_mgmt/v1/cluster_registrations", methods=["POST"])
def cluster_registrations():
    """"""
    example_request_body = {"authorization_token": "string", "cluster_id": "string"}

    # Check the headers
    try:
        token = process_headers(dict(request.headers))
    except MissingAuth:
        return "Authorization header missing", 401
    except BadBearerTokenValue:
        return "Invalid authorization header value", 401

    # Check the post body
    if request.method == "POST":
        user_data = request.form.to_dict()
    else:
        return "This endpoint only supports POST", 405

    # Check the request body
    cluster_id = user_data.get("cluster_id", None)
    authorization_token = user_data.get("authorization_token", None)
    if not (cluster_id and authorization_token):
        return "Body needs cluster_id and authorization_token", 400

    registration_response = {
        "account_id": str(uuid.uuid4()),
        "authorization_token": token,
        "cluster_id": cluster_id,
        "expires_at": "string",
    }
    return registration_response, 200


@accounts_mgmt.route("/api/accounts_mgmt/v1/accounts/<account>", methods=["GET"])
def get_accounts(account: str):
    # Inspect the header
    pass


@accounts_mgmt.route("/api/accounts_mgmt/v1/organizations/<org>", methods=["GET"])
def get_organizations(org: str):
    pass
