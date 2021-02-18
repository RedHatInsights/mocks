#!/usr/bin/env python3
import logging
import time

import keycloak

import crcmocks.config as conf


log = logging.getLogger(__name__)


class KeyCloakHelper:
    def __init__(self):
        self.server = conf.KEYCLOAK_URL
        self.username = conf.KEYCLOAK_USER
        self.password = conf.KEYCLOAK_PASSWORD
        self.realm = conf.KEYCLOAK_REALM
        self.client_base_url = conf.KEYCLOAK_CLIENT_BASE_URL

    def reload_conf(self):
        self.__init__()

    def wait_for_server(self):
        count = 1
        stop_time = time.time() + 30
        while time.time() < stop_time:
            log.info("attempt [%d] to connect to keycloak server '%s' ...", count, self.server)
            try:
                self._get_admin_object()
                break
            except Exception:
                log.exception("error connecting to keycloak server")
            count += 1
            time.sleep(1)
        else:
            raise Exception(f"failed to connect to keycloak server {self.server}")
        log.info("connected to keycloak server '%s' ...", self.server)

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

    @property
    def admin(self):
        return self._get_admin_object()

    @property
    def realm_admin(self):
        radmin = keycloak.KeycloakAdmin(
            self.server + "/auth/",
            realm_name=self.realm,
            user_realm_name="master",
            username=self.username,
            password=self.password,
            verify=False,
        )
        return radmin

    @property
    def openid(self):
        return keycloak.KeycloakOpenID(
            self.server + "/auth/",
            realm_name=self.realm,
            client_id=conf.KEYCLOAK_CLIENT_ID,
            verify=False,
        )

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

    def delete_all_realm_users(self):
        for user in self.get_realm_users():
            self.realm_admin.delete_user(user["id"])

    def create_realm_client(self, client):
        realm_client_names = self.get_realm_client_names()
        if client in realm_client_names:
            return

        protocol_mappers = [
            self.get_mapper("account_number", mtype="String"),
            self.get_mapper("account_id", mtype="String"),
            self.get_mapper("org_id", mtype="String"),
            self.get_mapper("username", mtype="String"),
            self.get_mapper("email", mtype="String"),
            self.get_mapper("first_name", mtype="String"),
            self.get_mapper("last_name", mtype="String"),
            self.get_mapper("is_org_admin", mtype="boolean"),
            self.get_mapper("is_internal", mtype="boolean"),
            self.get_mapper("is_active", mtype="boolean")
        ]

        # TODO: service accouts enabled == True, authorization enabled = True
        self.realm_admin.create_client(
            {
                "clientId": client,
                "enabled": True,
                "bearerOnly": False,
                "publicClient": True,
                "baseUrl": f"{self.client_base_url}",
                "redirectUris": [f"{self.client_base_url}/*"],
                "protocolMappers": protocol_mappers,
            }
        )

    def upsert_realm_user(self, uname, password, fname, lname, email, account_id, org_id, is_org_admin, is_internal, is_active):
        user_json = {
            "enabled": True,
            "username": uname,
            "firstName": fname,
            "lastName": lname,
            "email": email,
            "attributes": {
                "first_name": fname,
                "last_name": lname,
                "account_id": str(account_id),
                "account_number": str(account_id),
                "org_id": str(org_id),
                "is_internal": is_internal,
                "is_org_admin": is_org_admin,
                "is_active": is_active
            },
            "credentials": [{"temporary": False, "type": "password", "value": password}],
        }
        for user in self.get_realm_users():
            if user["username"] == uname:
                # user already exists
                user_id = user["id"]
                self.realm_admin.update_user(user_id, user_json)
                break
        else:
            # user does not already exist
            self.realm_admin.create_user(user_json)


kc_helper = KeyCloakHelper()
