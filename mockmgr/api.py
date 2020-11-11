#!/usr/bin/env python3

import os
import json
import time
from pprint import pprint

import requests
import keycloak


import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template_string

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from kchelper import KeyCloakHelper


USER_PAGE_TEMPLATE = ''' <!DOCTYPE HTML>
<html>
    <head>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <!--<pre>{{ rusers|tojson }}</pre>-->
        <table>
        <tr>
            <th>realm</th>
            <th>id</th>
            <th>username</th>
            <th>first_name</th>
            <th>last_name</th>
            <th>email</th>
            <th>org_id</th>
            <th>account_number</th>
        </tr>
        {% for ruser in rusers %}
            <tr>
                <td>{{ ruser.realm }}</td>
                <td>{{ ruser.id }}</td>
                <td>{{ ruser.username }}</td>
                <td>{{ ruser.attributes.first_name[0] }}</td>
                <td>{{ ruser.attributes.last_name[0] }}</td>
                <td>{{ ruser.email }}</td>
                <td>{{ ruser.attributes.org_id[0] }}</td>
                <td>{{ ruser.attributes.account_number[0] }}</td>
            <tr>
        {% endfor %}
        </table>
        <br>
        <a href='/adduser'>add user</a>
    </body>
</html>
'''


NEW_USER_FORM = '''<form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }} {{ form.username }}
        <p>
        <p>
            {{ form.email.label }} {{ form.email }}
        <p>
        </p>
            {{ form.first_name.label }} {{ form.first_name }}
        <p>
        </p>
            {{ form.last_name.label }} {{ form.last_name }}
        <p>
        </p>
            {{ form.account_number.label }} {{ form.account_number }}
        <p>
        </p>
            {{ form.org_id.label }} {{ form.org_id }}
        <p>
        </p>
            {{ form.password.label }}{{ form.password }}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
'''


class NewUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    org_id = IntegerField('org_id', validators=[DataRequired()])
    account_number = IntegerField('account_number', validators=[DataRequired()])
    submit = SubmitField('submit')


username = os.environ.get('KEYCLOAK_USERNAME', 'admin')
password = os.environ.get('KEYCLOAK_PASSWORD', 'admin')
server = os.environ.get('KEYCLOAK_URL', "http://keycloak:8080")
REALM = "redhat-external"
KH = KeyCloakHelper(server, username, password)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Skey12345'


@app.before_first_request
def create_initial_user():
    try:
        KH.create_realm_user(REALM, 'bob', 'redhat1234', 'bob', 'barker', 'bob@redhat.com', 1111, 1)
    except Exception as e:
        print(e)


@app.route('/')
def root():
    return render_template_string(USER_PAGE_TEMPLATE, rusers=KH.get_all_users())


@app.route('/realms/<realmname>')
def realms(realmname):
    rusers = KH.get_realm_users(realmname)
    return render_template_string(USER_PAGE_TEMPLATE, rusers=rusers)


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = NewUserForm()

    if request.method == 'POST':
        print(request.form)
        un = request.form.get('username')
        email = request.form.get('email')
        fn = request.form.get('first_name')
        ln = request.form.get('last_name')
        oi = request.form.get('org_id')
        an = request.form.get('account_number')
        pw = request.form.get('username')
        #create_realm_user(self, realm, uname, password, fname, lname, email, account_id, org_id):
        print('redhat-external', un, pw, fn, ln, email, an, oi)
        KH.create_realm_user(REALM, un, pw, fn, ln, email, an, oi)
        print('created ...')
        return redirect('/')

    return render_template_string(NEW_USER_FORM, form=form)
