from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template_string
from flask import url_for

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

from crcmocks.keycloak_helper import KeyCloakHelper
import crcmocks.config as conf


blueprint = Blueprint("manager", __name__)

USER_PAGE_TEMPLATE = """ <!DOCTYPE HTML>
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
        <a href='{{ redirect_url }}'>add user</a>
    </body>
</html>
"""


NEW_USER_FORM = """<form action="" method="post">
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
"""


class NewUserForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    first_name = StringField("first_name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    org_id = IntegerField("org_id", validators=[DataRequired()])
    account_number = IntegerField("account_number", validators=[DataRequired()])
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
    return render_template_string(
        USER_PAGE_TEMPLATE,
        redirect_url=url_for("manager.ui_adduser"),
        rusers=kc_helper.get_realm_users(),
    )


@blueprint.route("/ui/addUser", methods=["GET", "POST"])
def ui_adduser():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    form = NewUserForm()

    if request.method == "POST":
        un = request.form.get("username")
        email = request.form.get("email")
        fn = request.form.get("first_name")
        ln = request.form.get("last_name")
        oi = request.form.get("org_id")
        an = request.form.get("account_number")
        pw = request.form.get("password")
        kc_helper.create_realm_user(un, pw, fn, ln, email, an, oi)
        return redirect(url_for("manager.ui_root"))

    return render_template_string(NEW_USER_FORM, form=form)


@blueprint.route("/users")
def users():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    return jsonify(kc_helper.get_realm_users())


@blueprint.route("/addUser", methods=["POST"])
def user():
    if not conf.KEYCLOAK:
        return "keycloak integration is disabled", 501

    data = request.json(force=True)
    un = data.get("username")
    email = data.get("email")
    fn = data.get("first_name")
    ln = data.get("last_name")
    oi = data.get("org_id")
    an = data.get("account_number")
    pw = data.get("password")
    kc_helper.create_realm_user(un, pw, fn, ln, email, an, oi)
    return jsonify(kc_helper.get_realm_users())
