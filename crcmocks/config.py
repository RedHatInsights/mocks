import os


def env_bool(var_name, default):
    return str(os.getenv(var_name, default)).lower() == "true"


INITIALIZE_FE = env_bool("INITIALIZE_FE", False)
INITIALIZE_GW = env_bool("INITIALIZE_GW", False)
GW_MOCK_ENTITLEMENTS = env_bool("GW_MOCK_ENTITLEMENTS", True)
GW_MOCK_BOP = env_bool("GW_MOCK_BOP", True)

FE_DEPLOYMENT = os.getenv("FE_DEPLOYMENT", "front-end-aggregator")
GW_DEPLOYMENT = os.getenv("GW_DEPLOYMENT", "apicast")

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
KEYCLOAK_CLIENT_BASE_URL = os.getenv("KEYCLOAK_CLIENT_BASE_URL", f"https://{FE_DEPLOYMENT}")
KEYCLOAK_USER = os.getenv("KEYCLOAK_USER", "admin")
KEYCLOAK_PASSWORD = os.getenv("KEYCLOAK_PASSWORD", "admin")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "redhat-external")
KEYCLOAK = env_bool("KEYCLOAK", True)
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "cloud-services")
LOG_LEVEL = "INFO"
if os.getenv("LOG_LEVEL") in ["critical", "error", "warning", "info", "debug", "notset"]:
    LOG_LEVEL = os.getenv("LOG_LEVEL").upper()

PORT = int(os.getenv("PORT", 9000))

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(32))

DEFAULT_SERVICES = [
    "ansible",
    "cost_management",
    "insights",
    "advisor",
    "migrations",
    "openshift",
    "settings",
    "smart_management",
    "subscriptions",
    "user_preferences",
]

DEFAULT_PERMISSIONS = [
    "advisor:*:*",
    "compliance:*:*",
    "inventory:*:*",
    "migration-analytics:*:*",
    "patch:*:*",
    "policies:*:*",
    "remediations:*:*",
    "subscriptions:*:*",
    "vulnerability:*:*",
    "cost-management:*:*",
    "drift:*:*",
]

DEFAULT_USERS = [
    {
        "username": "jdoe",
        "id": 123456781,
        "account_number": "6089719",
        "email": "jdoe@acme.com",
        "first_name": "John",
        "last_name": "Doe",
        "address_string": '"John Doe" jdoe@acme.com',
        "is_active": False,
        "password": "redhat",
        "org_id": "3340852",
        "is_org_admin": False,
        "is_internal": False,
        "locale": "en_US",
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
    {
        "username": "org-admin",
        "id": 123456782,
        "account_number": "6089720",
        "email": "org-admin@acme.com",
        "first_name": "Org",
        "last_name": "Admin",
        "address_string": '"Org Admin" org-admin@acme.com',
        "is_active": True,
        "password": "redhat",
        "org_id": "3340853",
        "is_org_admin": True,
        "is_internal": True,
        "locale": "en_US",
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
    {
        "username": "non-org-admin",
        "id": 123456783,
        "account_number": "6089721",
        "email": "non-org-admin@acme.com",
        "first_name": "Non Org",
        "last_name": "Admin",
        "address_string": '"Non Org Admin" non-org-admin@acme.com',
        "is_active": True,
        "password": "redhat",
        "org_id": "3340854",
        "is_org_admin": False,
        "is_internal": False,
        "locale": "en_US",
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
    {
        "username": "iqe_rbac_admin",
        "id": 123456784,
        "account_number": "6089722",
        "email": "iqe_rbac_admin@redhat.com",
        "first_name": "RBAC",
        "last_name": "Admin",
        "address_string": '"RBAC Admin" iqe_rbac_admin@acme.com',
        "is_active": True,
        "password": "redhat",
        "is_org_admin": True,
        "is_internal": False,
        "locale": "en_US",
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
    {
        "username": "iqe_normal_user",
        "id": 123456785,
        "account_number": "6089723",
        "email": "iqe_normal_user@redhat.com",
        "first_name": "RBAC",
        "last_name": "Normal",
        "address_string": '"RBAC Normal" iqe_normal_user@acme.com',
        "is_active": True,
        "password": "redhat",
        "is_org_admin": False,
        "is_internal": False,
        "locale": "en_US",
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
    {
        "username": "iqe_rbac_on_rbac",
        "id": 123456786,
        "account_number": "6089724",
        "email": "iqe_rbac_on_rbac@redhat.com",
        "first_name": "RBAC",
        "last_name": "onRBAC",
        "address_string": '"RBAC onRBAC" iqe_rbac_on_rbac@acme.com',
        "is_active": True,
        "password": "redhat",
        "is_org_admin": False,
        "is_internal": False,
        "locale": "en_US",
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
]
