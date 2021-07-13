#!/usr/env/bin python
import json
import logging

from flask import Blueprint
from flask.json import jsonify
from flask import request

import crcmocks.config as conf
from crcmocks.keycloak_helper import kc_helper
from crcmocks.db import all_users

blueprint = Blueprint("bop", __name__)

log = logging.getLogger(__name__)

filter_maps = {
    "primaryEmail": ["email", "exact"],
    "emailStartsWith": ["email", "partial"],
    "principalStartsWith": ["username", "partial"],
    "users": ["username", "partial"],
    "status": ["is_active", "exact"],
    "admin_only": ["is_org_admin", "exact"]
}
value_maps = {
    "disabled": False,
    "enabled": True,
    "false": False,
    "true": True
}


def filter_fields(user_data_list, keys):
    # return only the fields valid for a BOP response
    data = []

    filters = dict(request.args)
    if request.data:
        filters.update(json.loads(request.data))

    filter_keys = list(filters.keys())

    for user in user_data_list:
        if len(filters) > 0:
            add = True

            for k in filter_keys:
                if k in filter_maps.keys():
                    [field, criteria] = filter_maps[k]
                    value = filters[k]

                    if not type(value) is list:
                        value = [value]

                    exact = False
                    partial = False
                    for v in value:
                        if v in value_maps.keys():
                            v = value_maps[v]

                        if not exact and not partial:
                            exact = v == user[field]
                            if type(user[field]) is str:
                                partial = user[field].startswith(v)

                    if criteria == "partial" and partial:
                        add = add and True
                    else:
                        if criteria == "exact" and exact:
                            add = add and True
                        else:
                            add = False

                if not add:
                    break

            if add:
                data.append({k: user[k] for k in keys})
        else:
            data.append({k: user[k] for k in keys})
            if "limit" in request.args:
                if len(data) == int(request.args.get("limit")):
                    break

    order = request.args.get("sortOrder")
    if order:
        data = sorted(data, key=lambda k: k["username"], reverse=(order == "des"))

    return data


@blueprint.route("/v1/users", methods=["POST"])
def mock_users():
    keys = [
        "username",
        "id",
        "account_number",
        "email",
        "first_name",
        "last_name",
        "address_string",
        "is_active",
        "is_org_admin",
    ]
    return jsonify(filter_fields(all_users(), keys))


@blueprint.route("/v1/accounts/<accountNumber>/usersBy", methods=["POST"])
def mock_users_by(accountNumber=None):
    keys = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "locale",
        "is_org_admin",
        "is_internal",
    ]
    return jsonify(filter_fields(all_users(), keys))


@blueprint.route("/v2/accounts/<accountNumber>/users", methods=["GET"])
def mock_accounts_v2(accountNumber=None):
    keys = [
        "username",
        "id",
        "account_number",
        "email",
        "first_name",
        "last_name",
        "locale",
        "is_active",
        "is_org_admin",
        "is_internal",
    ]
    return jsonify(filter_fields(all_users(), keys))


@blueprint.route("/v1/sendEmails", methods=["POST"])
def mock_send_email():
    return "sendEmails post requested"


@blueprint.route("/v1/jwt", methods=["GET"])
def mock_jwt():
    if conf.KEYCLOAK:
        pubkey = kc_helper.openid.public_key()
        return jsonify(
            {"pubkey": f"-----BEGIN PUBLIC KEY-----\n{pubkey}\n-----END PUBLIC KEY-----"}
        )
    return "keycloak integration disabled", 404
