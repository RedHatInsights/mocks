#!/usr/bin/env python3
import time

import keycloak
from cached_property import cached_property

import crcmocks.config as conf


class KeyCloakHelper:
    def __init__(self, server, username, password, realm, client_base_url):
        self.server = server
        self.username = username
        self.password = password
        self.realm = realm
        self.client_base_url = client_base_url

    def wait_for_server(self):
        count = 1
        stop_time = time.time() + 30
        while time.time() < stop_time:
            print("%s attempting keycloak connection to %s ..." % (count, self.server))
            try:
                self._get_admin_object()
                break
            except Exception as e:
                print(e)
            count += 1
            time.sleep(1)
        else:
            raise Exception(f"failed to connect to keycloak server {self.server}")
        print("connected to keycloak server %s" % self.server)

    def get_mapper(self, attribute, mtype="String"):
        mapper = {
            "name": attribute,
            "id": attribute,
            "protocol": "openid-connect",
            "protocolMapper": "oidc-usermodel-attribute-mapper",
            "consentRequired": False,
            "config": {
                "userinfo.token.claim": True,
                "user.attribute": attribute,
                "id.token.claim": True,
                "access.token.claim": True,
                "claim.name": attribute,
                "jsonType.label": mtype,
            },
        }
        return mapper

    def _get_admin_object(self):
        return keycloak.KeycloakAdmin(
            self.server + "/auth/", username=self.username, password=self.password, verify=False
        )

    @cached_property
    def admin(self):
        self.wait_for_server()
        return self._get_admin_object()

    @cached_property
    def realm_admin(self):
        self.wait_for_server()
        radmin = keycloak.KeycloakAdmin(
            self.server + "/auth/",
            realm_name=self.realm,
            user_realm_name="master",
            username=self.username,
            password=self.password,
            verify=False,
        )
        return radmin

    def get_realms(self):
        return self.admin.get_realms()

    def get_realm_names(self):
        realms = self.get_realms()
        realm_names = [x["realm"] for x in realms]
        return realm_names

    def create_realm(self):
        realm_names = self.get_realm_names()
        if self.realm not in realm_names:
            self.realm_admin.create_realm({"realm": self.realm, "enabled": True})

    def get_realm_clients(self):
        return self.realm_admin.get_clients()

    def get_realm_client_names(self):
        clients = self.get_realm_clients()
        client_names = [x["clientId"] for x in clients]
        return client_names

    def get_realm_users(self):
        return self.realm_admin.get_users()

    def create_realm_client(self, client):
        realm_client_names = self.get_realm_client_names()
        if client in realm_client_names:
            return

        protocol_mappers = [
            self.get_mapper("account_number", mtype="int"),
            self.get_mapper("account_id", mtype="int"),
            self.get_mapper("org_id", mtype="int"),
            self.get_mapper("username", mtype="String"),
            self.get_mapper("email", mtype="String"),
            self.get_mapper("first_name", mtype="String"),
            self.get_mapper("last_name", mtype="String"),
        ]

        # TODO: service accouts enabled == True, authorization enabled = True
        self.realm_admin.create_client(
            {
                "clientId": client,
                "enabled": True,
                "bearerOnly": False,
                "publicClient": True,
                "rootUrl": f"{self.client_base_url}",
                "baseUrl": f"{self.client_base_url}",
                "redirectUris": [f"{self.client_base_url}/*"],
                "protocolMappers": protocol_mappers,
            }
        )

    def create_realm_user(self, uname, password, fname, lname, email, account_id, org_id):
        self.realm_admin.create_user(
            {
                "enabled": True,
                "username": uname,
                "firstName": fname,
                "lastName": lname,
                "email": email,
                "attributes": {
                    "first_name": fname,
                    "last_name": lname,
                    "account_id": account_id,
                    "account_number": account_id,
                    "org_id": org_id,
                },
                "credentials": [{"temporary": False, "type": "password", "value": password}],
            }
        )


keycloak_helper = KeyCloakHelper(
    conf.KEYCLOAK_URL,
    conf.KEYCLOAK_USER,
    conf.KEYCLOAK_PASSWORD,
    conf.KEYCLOAK_REALM,
    conf.KEYCLOAK_CLIENT_BASE_URL,
)
