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
docker run -td --name mock-bop mocks:latest bop
```
* Entitlements:
```
docker run -td --name mock-entitlements mocks:latest entitlements
```
* RBAC:
```
docker run -td --name mock-rbac mocks:latest rbac
```
* Keycloak (SSO):
```
docker run -td --name keycloak -e DB_VENDOR=h2 -e PROXY_ADDRESS_FORWARDING=true -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin quay.io/keycloak/keycloak:latest
```

A special API called `mockmgr` provides a single interface for you to create/delete a user across
all the mock services. Start it with:
```
docker run -td --name mock-mgr mocks:latest mockmgr
```

## Running in OpenShift

Deploy the mock application into your namespace with:
```
oc process -f <app>/deploy.yaml | oc apply -f - -n <namespace>
```

You will also want to deploy the `mockmgr` so that you can create a test user in the mock apps.

The `keycloak` and `mockmgr` applications will expose an OpenShift route. The others do not.

