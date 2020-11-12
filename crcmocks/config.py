import os


KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
KEYCLOAK_CLIENT_BASE_URL = os.getenv("KEYCLOAK_CLIENT_BASE_URL", "https://front-end-aggregator")
KEYCLOAK_USER = os.getenv("KEYCLOAK_USER", "admin")
KEYCLOAK_PASSWORD = os.getenv("KEYCLOAK_PASSWORD", "admin")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "redhat-external")
KEYCLOAK = str(os.getenv("KEYCLOAK", True)).lower() == "true"
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "cloud-services")
LOG_LEVEL = "INFO"
if os.getenv("LOG_LEVEL") in ["critical", "error", "warning", "info", "debug", "notset"]:
    LOG_LEVEL = os.getenv("LOG_LEVEL").upper()

PORT = int(os.getenv("PORT", 9000))

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(32))

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
    }
]
