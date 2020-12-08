import logging

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from crcmocks.keycloak_helper import KeyCloakHelper
from crcmocks.util import get_users
import crcmocks.config as conf
import crcmocks.db


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


kc_helper = KeyCloakHelper(
    conf.KEYCLOAK_URL,
    conf.KEYCLOAK_USER,
    conf.KEYCLOAK_PASSWORD,
    conf.KEYCLOAK_REALM,
    conf.KEYCLOAK_CLIENT_BASE_URL,
)


@blueprint.route("/ui")
def ui_root():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501
    return render_template(
        "user_list.html",
        redirect_url=url_for("manager.ui_adduser"),
        rusers=get_users(),
    )


def add_user(user_data):
    un = user_data.get("username")
    email = user_data.get("email")
    fn = user_data.get("first_name")
    ln = user_data.get("last_name")
    oi = user_data.get("org_id")
    an = user_data.get("account_number")
    pw = user_data.get("password")

    # we don't add entitlements/permission to keycloak
    kc_helper.upsert_realm_user(un, pw, fn, ln, email, an, oi)
    crcmocks.db.add_user(user_data)
    log.info("added/updated user: %s", un)


def setup_keycloak():
    log.info("setting up keycloak...")
    kc_helper.wait_for_server()
    kc_helper.create_realm()
    kc_helper.create_realm_client(conf.KEYCLOAK_CLIENT_ID)
    kc_helper.delete_all_realm_users()
    for user in conf.DEFAULT_USERS:
        add_user(user)


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
