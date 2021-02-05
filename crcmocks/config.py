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
    "vulnerability:*:*"
]

DEFAULT_USERS = [
    {
        "username": "jdoe",
        "id": 123456701,
        "account_number": "0369234",
        "email": "jdoe@acme.com",
        "first_name": "John",
        "last_name": "Doe",
        "address_string": '"John Doe" jdoe@acme.com',
        "is_active": True,
        "password": "redhat",
        "org_id": "3340852",
        "is_org_admin": False,
        "is_internal": False,
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    },
    {
        "username": "org-admin",
        "id": 12345678,
        "account_number": "0369235",
        "email": "org-admin@acme.com",
        "first_name": "Org",
        "last_name": "Admin",
        "address_string": '"Org Admin" org-admin@acme.com',
        "is_active": True,
        "password": "redhat",
        "org_id": "3340853",
        "is_org_admin": True,
        "is_internal": True,
        "entitlements": ",".join(DEFAULT_SERVICES),
        "permissions": ",".join(DEFAULT_PERMISSIONS),
    }
]
