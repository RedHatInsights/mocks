#/usr/bin/env python3

import os

import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect


app = Flask(__name__)


services = [
    'ansible',
    'cost_management',
    'insights',
    'migrations',
    'openshift',
    'settings',
    'smart_management',
    'subscriptions',
    'user_preferences'
]


entitlements = {}
for svc in services:
    entitlements[svc] = {'is_entitled': True, 'is_trial': False}


@app.route('/api/entitlements/v1/services')
def services():
    return jsonify(entitlements)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
