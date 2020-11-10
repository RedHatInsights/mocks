#!/usr/env/bin python
import json
import logging
from multiprocessing import Process
from time import strftime

from flask import Flask
from flask import request

app = Flask(__name__)
log = logging.getLogger(__name__)

request_data_list = []

user_data_list = [
    ["jdoe", 123456701, "0369234", "jdoe@acme.com", "John", "Doe", '"John Doe" jdoe@acme.com'],
    [
        "jdoe2",
        123456702,
        "3340852",
        "jdoe2@acme.com",
        "John",
        "Doetwo",
        '"John Doetwo" jdoe2@acme.com',
    ],
    [
        "jdoe3",
        123456703,
        "0369244",
        "jdoe3@acme.com",
        "John",
        "Doethree",
        '"John Doethree" jdoe3@acme.com',
    ],
    [
        "jdoe4",
        123456704,
        "0369244",
        "jdoe4@acme.com",
        "John",
        "Doefour",
        '"John Doefour" jdoe4@acme.com',
    ],
]


def start_flask():
    app.run(host="0.0.0.0", port=8080, debug=True)


def build_user_data(user_data_list):
    user_data = []
    ach_data = {}
    for data in user_data_list:
        ach_data[data[0]] = {
            "username": data[0],
            "id": data[1],
            "account_number": data[2],
            "email": data[3],
            "first_name": data[4],
            "last_name": data[5],
            "address_string": data[6],
            "is_active": True,
        }
    user_data.append(ach_data)
    return user_data


@app.route("/users", methods=["POST"])
def mock_user():
    data = []
    for user in build_user_data(user_data_list):
        for key, value in user.items():
            data.append(value)
    return json.dumps(data)


@app.route("/sendEmails", methods=["POST"])
def mock_send_email():
    return "sendEmails post requested"


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
    request_data_list.append(request_info)
    return response


@app.route("/getRequests")
def get_request_data():
    return json.dumps(request_data_list)


@app.route("/clearRequests")
def clear_request_data():
    global request_data_list
    request_data_list = []
    return json.dumps([])


@app.route("/shutdown", methods=["POST"])
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
