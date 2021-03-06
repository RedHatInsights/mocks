#!/usr/env/bin python
import logging

from flask import Blueprint
from flask.json import jsonify

import crcmocks.config as conf
from crcmocks.keycloak_helper import kc_helper
from crcmocks.db import all_users

blueprint = Blueprint("bop", __name__)

log = logging.getLogger(__name__)


def filter_fields(user_data_list):
    # return only the fields valid for a BOP response
    data = []
    keys = [
        "username",
        "id",
        "account_number",
        "email",
        "first_name",
        "last_name",
        "address_string",
        "is_active",
    ]
    for user in user_data_list:
        data.append({k: user[k] for k in keys})
    return data


@blueprint.route("/v1/users", methods=["POST"])
def mock_users():
    return jsonify(filter_fields(all_users()))


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
