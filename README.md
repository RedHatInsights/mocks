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
docker run -td --name mock-bop mocks:latest /mocks/bop/api.py
```
* Entitlements:
```
docker run -td --name mock-entitlements mocks:latest /mocks/entitlements/api.py
```
* RBAC:
```
docker run -td --name mock-rbac mocks:latest /mocks/rbac/api.py
```
* Keycloak (SSO):
```
docker run -td --name keycloak -e DB_VENDOR=h2 -e PROXY_ADDRESS_FORWARDING=true -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin quay.io/keycloak/keycloak:latest
docker run -td --name keycloak-admin mocks:latest /mocks/keycloak/keycloak_admin/api.py
```
