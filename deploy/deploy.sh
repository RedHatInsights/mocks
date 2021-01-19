#!/bin/bash
set -e

NS=$(oc project -q)

echo "Deploying mocks to namespace $NS"

read -p "Are you sure? " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 0
fi

oc process -f template.yaml --local=true | oc apply -f - -n $NS

echo "Use the following routes: "
oc get route -o jsonpath="{range .items[*]}https://{.spec.host}{'\n'}"
