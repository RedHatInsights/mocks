from flask import jsonify
from flask import Blueprint


blueprint = Blueprint("entitlements", __name__)


services = [
    "ansible",
    "cost_management",
    "insights",
    "advisor",
    "migrations",
    "openshift",
    "settings",
    "smart_management",
    "subscriptions",
    "user_preferences",
]
entitlements = {}
for svc in services:
    entitlements[svc] = {"is_entitled": True, "is_trial": False}


@blueprint.route("/v1/services")
def services():
    return jsonify(entitlements)
