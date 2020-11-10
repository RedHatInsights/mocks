Mock services for testing cloud.redhat.com applications

# Usage

## Running locally

First build the base image:
```
docker build -t mocks .
```

Then use the following commands depending on the mock you want to run:
* BOP:
```
docker run --name mock-bop -td /mocks/bop/api.py
```
* Entitlements:
```
docker run --name mock-entitlements -td /mocks/entitlements/api.py
```
* RBAC:
```
docker run --name mock-rbac -td /mocks/rbac/api.py
```
* Keycloak (SSO):
```
docker run --name keycloak -td -e DB_VENDOR=h2 -e PROXY_ADDRESS_FORWARDING=true -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin
docker run --name keycloak-admin -td /mocks/keycloak/keycloak_admin/api.py
```
