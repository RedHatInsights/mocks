# About

Mock services for testing cloud.redhat.com applications

This is project offers a solution for mocking out certain service dependencies such as BOP, RBAC, entitlements, and SSO.

It relies on two pieces:
* crcmocks -- a collection of flask APIs that replace BOP, RBAC, entitlements APIs, interact with a `keycloak` deployment to set up SSO, and provide user management APIs so you can add additional users for testing.
* keycloak -- a generic deployment of keycloak, which `crcmocks` will interact with and provision for you

# Usage

See the `Deploying` section below for information on how to deploy locally or on OpenShift.

When `crcmocks` starts up, it uses options defined in its [config](crcmocks/config.py) to connect to a keycloak deployment and provision a realm, client, and users in the SSO backend.

Once you have the `crcmocks` API service running (it listens on port 9000 by default) the following APIs are provided:

### Management APIS

* `GET /_getRequests` -- returns a list of all API requests that have come into the `crcmocks` service
* `POST /_clearRequests` -- clears the stored list of all API requests
* `POST /_shutdown` -- shuts down the flask API
* `GET /_manager/user` -- returns an HTML form you can use to create a new user. You can browse to this URL on a web browser.
* `POST /_manager/addUser` -- allows you to create new test user with JSON
* `GET /_manager/users` -- returns JSON listing all users created in the backend

### Management UI

* `GET /_manager/ui` -- allows you to see which users have been created and add new users via a web browser

### RBAC
* `GET /api/rbac/v1/access/` -- returns a pre-canned response stating the user has access to `insights:*:*`

### Entitlements
* `GET /api/entitlements/v1/services` -- returns a canned response stating the user is entitled for a variety of services

### BOP
* `POST /api/bop/v1/users` -- returns a mocked BOP response listing all users that have been created in `crcmocks`
* `GET /api/bop/v1/jwt` -- if keycloak is in use, returns the pubkey for the realm configured on the local keycloak deployment. Else, returns the IT CA public cert.
* `GET /api/bop/v1/sendEmails` -- accepts a POST and simply stores the incoming request so it can be read later, allowing you to test if your application sent an email to the right users with the right subject/body/etc.

# Deploying

## Running locally

First build the base image:
```
docker build -t mocks .
```

Then start two containers:
* Keycloak (SSO):
```
docker run -td --name keycloak -p 8080:8080 -e DB_VENDOR=h2 -e PROXY_ADDRESS_FORWARDING=true -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin quay.io/keycloak/keycloak:latest
```
* Mock APIs:
```
docker run -td --name mocks -p 9000:9000 -e KEYCLOAK_URL="http://localhost:8080" mocks:latest
```

You can also pull the mocks image from `quay.io/cloudservices/mocks` if you don't wish to build it.

You will then need to point your application to use `localhost:9000` for BOP, RBAC, and
entitlements API requests. You will need to update your running copy of `insights-chrome` to point
to `localhost:8080` as the SSO URL instead of `sso.qa.redhat.com`. To do this you can edit [this file](https://github.com/RedHatInsights/insights-chrome/blob/master/src/js/jwt/insights/url.js)
and re-build chrome with `npm run build`.


## Running in OpenShift

Deploy an ephemeral instance of the front-end, gateway, and any other backend apps you want from [e2e-deploy](https://www.github.com/RedHatInsights/e2e-deploy) using
ocdeployer. Example:

```
ocdeployer deploy -c -e smoke -s advisor,platform-mq,ingress,inventory,engine,gateway,front-end-aggregator --secrets-src-project secrets MYPROJECT
```

Deploy the mock application into your namespace with:
```
cd deploy && ./deploy.sh
```

The deploy script will do the following:
1. update the 3scale configs to use the mock APIs deployed in this namespace (BOP, entitlements)
2. deploy the `mocks` and `keycloak` containers into a single deployment named "mocks"
3. set up `Service` objects for `rbac:8080` and `entitlements-api-go:3000` to route to the mock APIs
4. set up `Route` objects for `keycloak` and the `mocks` containers
5. update chrome in the front-end-aggregator deployment to use the mock SSO

The end result is you should be able to browse to your front-end-aggregator URL and log in using mock SSO

You can access the mock user management APIs as described above via the mock `Route` URL


# TODO

* Allow users to be created with dynamic RBAC permissions and/or entitlements