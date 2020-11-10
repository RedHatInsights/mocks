#/usr/bin/env python3

import os

import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect


app = Flask(__name__)


rbac = {
    'meta': {'count': 30, 'limit': 1000, 'offset': 0},
    'links': {
        'first': '/api/rbac/v1/access/?application=&format=json&limit=1000&offset=0',
        'next': None,
        'previous': None,
        'last': '/api/rbac/v1/access/?application=&format=json&limit=1000&offset=0',
    },
    'data': [
        {'resourceDefinitions': [], 'permission': 'insights:*:*'}
    ]
}


@app.route('/api/rbac/v1/access/')
def rbac_access():
    return jsonify(rbac)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
