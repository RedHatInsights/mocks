from copy import deepcopy

from flask import jsonify
from flask import Blueprint
from flask import request

# Mocks of some basic OCM API endpoints needed for testing uhc-auth-proxy

blueprint = Blueprint("ocm", __name__)


def process_headers(headers):
    """ Confirms the headers are structurally valid. """
    pass


@blueprint.route("/api/accounts_mgmt/v1/cluster_registrations", methods=["GET"])
def cluster_registrations():
    """
    Mock of the OCM endpoint
    """
    # Inspect the header
    pass


@blueprint.route("/api/accounts_mgmt/v1/accounts/<account>", methods=["GET"])
def get_accounts(account: str):
    # Inspect the header
    pass


@blueprint.route("/api/accounts_mgmt/v1/organizations/<org>", methods=["GET"])
def get_organizations(org: str):
    pass


