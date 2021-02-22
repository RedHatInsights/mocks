import logging

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Optional

import crcmocks.config as conf
import crcmocks.db
from crcmocks.keycloak_helper import kc_helper
from crcmocks.util import get_users


log = logging.getLogger(__name__)
blueprint = Blueprint("manager", __name__)


class NewUserForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    first_name = StringField("first_name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    org_id = IntegerField("org_id", validators=[DataRequired()])
    account_number = IntegerField("account_number", validators=[DataRequired()])
    # if these fields are None, they will return the DEFAULT values in the response
    entitlements = StringField("entitlements", default=None, validators=[Optional()])
    permissions = StringField("permissions", default=None, validators=[Optional()])
    submit = SubmitField("submit")


@blueprint.route("/ui")
def ui_root():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501
    return render_template(
        "user_list.html",
        redirect_url=url_for("manager.ui_adduser"),
        rusers=get_users(),
    )


def add_user(user_data, skip_if_exists=False):
    un = user_data.get("username")
    email = user_data.get("email")
    fn = user_data.get("first_name")
    ln = user_data.get("last_name")
    oi = user_data.get("org_id")
    an = user_data.get("account_number")
    pw = user_data.get("password")
    io = user_data.get("is_org_admin")
    ii = user_data.get("is_internal")
    ia = user_data.get("is_active")

    # we don't add entitlements/permissions to keycloak
    kc_helper.upsert_realm_user(un, pw, fn, ln, email, an, oi, io, ii, ia, skip_if_exists)
    crcmocks.db.add_user(user_data, skip_if_exists)


def setup_keycloak():
    log.info("setting up keycloak...")
    kc_helper.wait_for_server()
    kc_helper.create_realm()
    kc_helper.create_realm_client(conf.KEYCLOAK_CLIENT_ID)
    for user in conf.DEFAULT_USERS:
        add_user(user, skip_if_exists=True)


@blueprint.route("/ui/addUser", methods=["GET", "POST"])
def ui_adduser():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    form = NewUserForm()

    if request.method == "POST":
        user_data = request.form.to_dict()
        add_user(user_data)
        return redirect(url_for("manager.ui_root"))

    return render_template("new_user_form.html", form=form)


@blueprint.route("/users")
def users():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    return jsonify(get_users())


@blueprint.route("/addUser", methods=["POST"])
def user():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    user_data = request.json(force=True)
    add_user(user_data)
    return jsonify(get_users())


@blueprint.route("/resetUsers", methods=["POST"])
def reset_users():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    kc_helper.delete_all_realm_users()
    crcmocks.db.clear_users()

    setup_keycloak()
    return jsonify(get_users())
