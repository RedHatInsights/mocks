export IMAGE="quay.io/cloudservices/mocks"  # the image location on quay

# Install bonfire repo/initialize
CICD_URL=https://raw.githubusercontent.com/RedHatInsights/bonfire/master/cicd
curl -s $CICD_URL/bootstrap.sh > .cicd_bootstrap.sh && source .cicd_bootstrap.sh

# Build the image and push to quay
source $CICD_ROOT/build.sh

# Test that the deployment works
source ${CICD_ROOT}/_common_deploy_logic.sh
export NAMESPACE=$(bonfire namespace reserve)
bonfire deploy \
    gateway insights-ephemeral \
    --source=appsre \
    --set-template-ref mocks=${GIT_COMMIT} \
    --set-image-tag ${IMAGE}=${IMAGE_TAG} \
    --namespace ${NAMESPACE} \

# Create a 'dummy' junit result file so Jenkins will not fail
mkdir -p $WORKSPACE/artifacts
cat << EOF > $WORKSPACE/artifacts/junit-dummy.xml
<testsuite tests="1">
    <testcase classname="dummy" name="dummytest"/>
</testsuite>
EOF
