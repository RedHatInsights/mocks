#!/usr/env/bin python
import logging
from time import strftime

from flask import Flask
from flask import request
from flask.json import jsonify

from crcmocks.bop import blueprint as bop_bp
from crcmocks.rbac import blueprint as rbac_bp
from crcmocks.entitlements import blueprint as entitlements_bp
from crcmocks.manager import blueprint as manager_bp
from crcmocks.manager import setup_keycloak
import crcmocks.config as conf
import crcmocks.db


log = logging.getLogger(__name__)


app = Flask(__name__)
app.config["SECRET_KEY"] = conf.SECRET_KEY
app.register_blueprint(bop_bp, url_prefix="/api/bop")
app.register_blueprint(entitlements_bp, url_prefix="/api/entitlements")
app.register_blueprint(rbac_bp, url_prefix="/api/rbac")
app.register_blueprint(manager_bp, url_prefix="/_manager")


def start_flask():
    logging.basicConfig(level=getattr(logging, conf.LOG_LEVEL))
    if conf.KEYCLOAK:
        setup_keycloak()
    app.run(host="0.0.0.0", port=conf.PORT, debug=True)


@app.after_request
def store_request(response):
    global request_data_list
    ts = strftime("[%Y-%b-%d %H:%M]")
    request_info = {
        "timestamp": ts,
        "method": request.method,
        "path": request.path,
        "data": request.data.decode("utf-8"),
        "response_status": response.status,
        "response_data": response.data.decode("utf-8"),
    }
    crcmocks.db.add_request(request_info)
    return response


@app.route("/_getRequests")
def get_request_data():
    return jsonify(crcmocks.db.all_requests())


@app.route("/_clearRequests", methods=["POST"])
def clear_request_data():
    crcmocks.db.clear_requests()
    return jsonify([])


@app.route("/_shutdown", methods=["POST"])
def shutdown_server():
    log.info("Shutdown context hit with POST!")
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if shutdown is None:
        raise RuntimeError("The function is unavailable!")
    else:
        shutdown()
        return "The server is shutting down!"


if __name__ == "__main__":
    start_flask()
