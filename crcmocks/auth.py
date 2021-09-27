#!/usr/env/bin python
import logging

from flask import Blueprint
from flask.json import jsonify
from flask_httpauth import HTTPBasicAuth
from keycloak.exceptions import KeycloakAuthenticationError

import crcmocks.config as conf
from crcmocks.keycloak_helper import kc_helper

blueprint = Blueprint("auth", __name__)
log = logging.getLogger(__name__)
auth = HTTPBasicAuth()


@blueprint.route("/v1/auth", methods=["GET"])
def mock_basic_auth():
    if not conf.KEYCLOAK:
        return "keycloak integration disabled", 404

    creds = auth.get_auth()

    # https://github.com/RedHatInsights/insights-3scale/blob/master/build/docker-assets/src/insights/identity.lua#L93
    try:
        token = kc_helper.openid.token(creds['username'], creds['password'])
    except KeycloakAuthenticationError:
        return "Unauthorized", 401

    userinfo = kc_helper.openid.userinfo(token['access_token'])

    return jsonify({ 'user': userinfo })
