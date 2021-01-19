import uuid

from flask import jsonify
from flask import Blueprint
from flask import request

# Mocks of some basic accounts_mgmt API endpoints needed for testing uhc-auth-proxy
# API ref: https://api.openshift.com/?urls.primaryName=Accounts%20management%20service
from crcmocks.accounts_mgmt_db.accessors import get_org_by_id, get_account_by_id

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

    # TODO: Some sort of look up to get the account_id related to the auth token?
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
    try:
        token = process_headers(dict(request.headers))
    except MissingAuth:
        return "Authorization header missing", 401
    except BadBearerTokenValue:
        return "Invalid authorization header value", 401
    pass

    # Check the request type
    if request.method != "GET":
        return "This endpoint only supports GET", 405

    # TODO: Get account, see if it exists. If it doesn't, return a 404.
    account_details = get_account_by_id(account)
    if not account_details:
        return f"Account with id {account} does not exist", 404

    # TODO: Get the org id for the specified account

    # TODO: Identify the fields that uhc-auth-proxy actually cares about
    example_response = {
        "kind": "string",
        "page": 0,
        "size": 1,
        "total": 1,
        "items": [
            {
                "href": "string",
                "id": "string",
                "kind": "string",
                "ban_code": "string",
                "ban_description": "string",
                "banned": False,
                "capabilities": [
                    {
                        "href": "string",
                        "id": "string",
                        "kind": "string",
                        "inherited": True,
                        "name": "string",
                        "value": "string",
                    }
                ],
                "created_at": "2021-01-14T18:51:47.487Z",
                "email": "user@example.com",
                "first_name": "string",
                "labels": [
                    {
                        "href": "string",
                        "id": "string",
                        "kind": "string",
                        "account_id": "string",
                        "created_at": "2021-01-14T18:51:47.487Z",
                        "internal": True,
                        "key": "string",
                        "organization_id": "string",
                        "subscription_id": "string",
                        "type": "string",
                        "updated_at": "2021-01-14T18:51:47.487Z",
                        "value": "string",
                    }
                ],
                "last_name": "string",
                "organization": {
                    "href": "string",
                    # This is the value that uhc-auth-proxy cares about
                    "id": "string",
                    "kind": "string",
                    "capabilities": [
                        {
                            "href": "string",
                            "id": "string",
                            "kind": "string",
                            "inherited": True,
                            "name": "string",
                            "value": "string",
                        }
                    ],
                    "created_at": "2021-01-14T18:51:47.488Z",
                    "ebs_account_id": "string",
                    "external_id": "string",
                    "labels": [
                        {
                            "href": "string",
                            "id": "string",
                            "kind": "string",
                            "account_id": "string",
                            "created_at": "2021-01-14T18:51:47.488Z",
                            "internal": True,
                            "key": "string",
                            "organization_id": "string",
                            "subscription_id": "string",
                            "type": "string",
                            "updated_at": "2021-01-14T18:51:47.488Z",
                            "value": "string",
                        }
                    ],
                    "name": "string",
                    "updated_at": "2021-01-14T18:51:47.488Z",
                },
                "organization_id": "string",
                "service_account": False,
                "updated_at": "2021-01-14T18:51:47.488Z",
                "username": "string",
            }
        ],
    }
    return jsonify(example_response), 200


@accounts_mgmt.route("/api/accounts_mgmt/v1/organizations/<org>", methods=["GET"])
def get_organizations(org: str):
    """
    Get organization by org_id
    """
    # Inspect the header
    try:
        token = process_headers(dict(request.headers))
    except MissingAuth:
        return "Authorization header missing", 401
    except BadBearerTokenValue:
        return "Invalid authorization header value", 401

    if request.method != "GET":
        return "This endpoint only supports GET", 405

    # TODO: Consider adding some temporary persistence and look-up logic to make this more realistic
    org_details = get_org_by_id(org)

    # The main values uhc-auth-proxy cares about are ebs_account_id and external_id
    ebs_account_id = org_details.get("ebs_account")
    external_id = org_details.get("external_id")
    example_response = {
        "href": "string",
        "id": "string",
        "kind": "string",
        "capabilities": [
            {
                "href": "string",
                "id": "string",
                "kind": "string",
                "inherited": True,
                "name": "string",
                "value": "string",
            }
        ],
        "created_at": "2021-01-14T19:23:28.922Z",
        "ebs_account_id": ebs_account_id,
        "external_id": external_id,
        "labels": [
            {
                "href": "string",
                "id": "string",
                "kind": "string",
                "account_id": "string",
                "created_at": "2021-01-14T19:23:28.922Z",
                "internal": True,
                "key": "string",
                "organization_id": "string",
                "subscription_id": "string",
                "type": "string",
                "updated_at": "2021-01-14T19:23:28.922Z",
                "value": "string",
            }
        ],
        "name": "string",
        "updated_at": "2021-01-14T19:23:28.922Z",
    }
    return jsonify(example_response), 200
