#!/bin/bash
set -e

NS=$(oc project -q)
CONF_FILE="apicast-insights-3cale-config-ephemeral-for-mocks.yaml"

echo "Deploying mocks to namespace $NS"

read -p "Are you sure? " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 0
fi

# If 'apicast' is present in the namespace, modify its config ...
if [ ! -z "$(oc get dc apicast)" ]; then
    echo "Updating apicast 3scale config..."
    ENTITLEMENTS_CONF=$(sed "s/NAMESPACE/${NS}/g" 3scale-insights-entitlements.json | base64 -w0)
    SERVICES_CONF=$(sed "s/NAMESPACE/${NS}/g" 3scale-insights-services.json | base64 -w0)
    NEW_CONF_DATA=$(
        sed \
        -e "s/ENTITLEMENTS_CONF/${ENTITLEMENTS_CONF}/g" \
        -e "s/SERVICES_CONF/${SERVICES_CONF}/g" \
        $CONF_FILE
    )
    echo "$NEW_CONF_DATA" | oc apply -f - -n $NS
    oc rollout latest dc/apicast
    oc rollout status dc/apicast
fi

# If we are able to see a route for 'front-end-aggregator' in our namespace, have crcmocks set up
# the keycloak cloud-services client with the proper redirect URI
FE_HOST=$(oc get route front-end-aggregator -o jsonpath='{.spec.host} -n $NS')
FE_URL="https://${FE_HOST}"
if [ ! -z "$FE_HOST" ]; then
    oc process -f template.yaml -p KEYCLOAK_CLIENT_BASE_URL=$FE_URL --local=true | oc apply -f - -n $NS
else
    oc process -f template.yaml --local=true | oc apply -f - -n $NS
fi

kubectl rollout restart deploy/mocks
oc rollout status deploy/mocks

if [ ! -z "$FE_HOST" ]; then
    # modify chrome.js to point to our keycloak deployment
    echo "Updating chrome.js SSO url..."
    QA_HOST="sso.qa.redhat.com"
    KEYCLOAK_HOST=$(oc get route keycloak -o jsonpath='{.spec.host}' -n $NS)
    CHROME_JS="/all/code/chrome/js/chrome.*.js"
    POD=$(oc get pod -l app=front-end-aggregator -o jsonpath='{.items[0].metadata.name}')
    oc exec $POD -- /bin/bash -c "sed -i 's/$QA_HOST/$KEYCLOAK_HOST/g' $CHROME_JS"
    oc exec $POD -- /bin/bash -c "rm $CHROME_JS.gz && gzip --keep $CHROME_JS"
fi

echo "Use the following routes: "
oc get route -o jsonpath="{range .items[*]}https://{.spec.host}{'\n'}"
