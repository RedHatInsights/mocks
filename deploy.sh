#!/bin/bash

# Have crcmocks set up the keycloak cloud-services client with the proper redirect URI if
# we are able to see a route for 'front-end-aggregator' in our namespace

set -exv

FE_HOST=$(oc get route front-end-aggregator -o jsonpath='{.spec.host}')

if [ ! -z "$FE_HOST" ]; then
    oc process -f deploy.yaml -p KEYCLOAK_CLIENT_BASE_URL="https://${FE_HOST}" | oc apply -f -
else
    oc process -f deploy.yaml | oc apply -f -
fi

