from flask import jsonify
from flask import Blueprint


blueprint = Blueprint("rbac", __name__)

rbac_response = {
    "meta": {"count": 30, "limit": 1000, "offset": 0},
    "links": {
        "first": "/api/rbac/v1/access/?application=&format=json&limit=1000&offset=0",
        "next": None,
        "previous": None,
        "last": "/api/rbac/v1/access/?application=&format=json&limit=1000&offset=0",
    },
    "data": [{"resourceDefinitions": [], "permission": "insights:*:*"}],
}


@blueprint.route("/v1/access/")
def rbac_access():
    return jsonify(rbac_response)
