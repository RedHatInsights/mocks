#!/usr/env/bin python
import logging
from multiprocessing import Process
from time import strftime

from flask import Blueprint
from flask.json import jsonify

import crcmocks.config as conf

blueprint = Blueprint("bop", __name__)

log = logging.getLogger(__name__)


def build_user_data(user_data_list):
    user_data = []
    ach_data = {}
    for data in user_data_list:
        ach_data[data["username"]] = {
            "username": data["username"],
            "id": data["id"],
            "account_number": data["account_number"],
            "email": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "address_string": data["address_string"],
            "is_active": data["is_active"],
        }
    user_data.append(ach_data)
    return user_data


@blueprint.route("/v1/users", methods=["POST"])
def mock_users():
    data = []
    for user in build_user_data(conf.USERS):
        for key, value in user.items():
            data.append(value)
    return jsonify(data)


@blueprint.route("/v1/sendEmails", methods=["POST"])
def mock_send_email():
    return "sendEmails post requested"


@blueprint.route("/v1/jwt", methods=["GET"])
def mock_jwt():
    pass
