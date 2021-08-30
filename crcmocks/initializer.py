import base64
import json
import logging

from ocviapy import get_associated_pods
from ocviapy import get_json
from ocviapy import oc
from ocviapy import scale_down_up

import crcmocks.config as conf
from crcmocks.keycloak_helper import kc_helper


log = logging.getLogger(__name__)


INITIALIZED = False


def create_service(namespace, name, src_port):
    """
    Create a Service resource that points the name/src_port towards the mocks pod
    """
    svc = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name},
        "spec": {
            "ports": [
                {"name": f"{src_port}-tcp", "port": src_port, "protocol": "TCP", "targetPort": 9000}
            ],
            "selector": {"app": "mocks", "name": "mocks"},
            "sessionAffinity": "None",
            "type": "ClusterIP",
        },
    }
    oc("apply", "-f", "-", "-n", namespace, _in=json.dumps(svc))


def initialized():
    return INITIALIZED


def initialize():
    global INITIALIZED

    namespace = None
    if conf.INITIALIZE_FE or conf.INITIALIZE_GW:
        log.info("Initializing k8s environment...")
        try:
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as fp:
                namespace = fp.readlines()[0].strip()
        except OSError:
            log.error("Unable to load namespace file, are we running in kubernetes?")
            raise

    if conf.INITIALIZE_FE:
        initialize_fe(namespace)
    if conf.INITIALIZE_GW:
        initialize_gw(namespace)
    if conf.MOCK_RBAC:
        create_service(namespace, "rbac", 8080)
    if conf.MOCK_ENTITLEMENTS:
        create_service(namespace, "entitlements-api-go", 3000)

    INITIALIZED = True


def initialize_fe(namespace):
    """
    When running in k8s, initialize the front-end-aggregator deployment
    """
    # Use the fe deployment's hostname as our KEYCLOAK_CLIENT_BASE_URL
    log.info("Setting our keycloak_client_base_url to match front-end-aggregator route...")
    fe_host = get_json("route", conf.FE_DEPLOYMENT, namespace=namespace).get("spec", {}).get("host")
    if not fe_host:
        raise Exception(f"Unable to find route for {conf.FE_DEPLOYMENT}")
    conf.KEYCLOAK_CLIENT_BASE_URL = f"https://{fe_host}"
    kc_helper.reload_conf()

    # Modify chrome.js to point to our keycloak deployment
    log.info("Updating chrome.js SSO url on deployment %s", conf.FE_DEPLOYMENT)
    fe_pods = get_associated_pods(namespace, "deployment", conf.FE_DEPLOYMENT).get("items")
    if not fe_pods:
        raise Exception(f"Unable to find pods for deployment {conf.FE_DEPLOYMENT}")

    qa_host = "sso.qa.redhat.com"

    keycloak_host = get_json("route", "keycloak", namespace=namespace).get("spec", {}).get("host")
    if not keycloak_host:
        raise Exception("Unable to find route named 'keycloak'")

    fe_pod = fe_pods[0]["metadata"]["name"]
    cmd = (
        f"cd /all/code/chrome/js && "
        "for f in `ls *.js`; "
        f"do sed -i s/{qa_host}/{keycloak_host}/g $f && "
        "rm $f.gz && "
        "gzip --keep $f; "
        "done"
    )

    oc("exec", fe_pod, "-n", namespace, "--", "/bin/bash", "-c", cmd)


def initialize_gw(namespace):
    gw_deployment = get_json("deployment", conf.GW_DEPLOYMENT, namespace=namespace)
    if not gw_deployment:
        raise Exception(f"Unable to find deployment {conf.GW_DEPLOYMENT}")

    secret = get_json("secret", "apicast-insights-3scale-config")

    if conf.MOCK_ENTITLEMENTS:
        log.info("Updating gateway config to use mock entitlements")

        entitlements_conf = json.loads(
            base64.urlsafe_b64decode(secret["data"]["insights_entitlements.json"])
        )
        entitlements_conf["ephemeral"]["host"] = (
            f"http://entitlements-api-go.{namespace}.svc.cluster.local:3000/"
            "api/entitlements/v1/services"
        )
        secret["data"]["insights_entitlements.json"] = base64.urlsafe_b64encode(
            json.dumps(entitlements_conf).encode()
        ).decode()

    if conf.MOCK_BOP:
        log.info("Updating gateway config to use mock BOP")
        services_conf = json.loads(
            base64.urlsafe_b64decode(secret["data"]["insights_services.json"])
        )
        services_conf["ephemeral"][
            "services_host"
        ] = f"http://mocks.{namespace}.svc.cluster.local:8080"
        services_conf["ephemeral"]["jwt_path"] = "/api/bop/v1/jwt"
        secret["data"]["insights_services.json"] = base64.urlsafe_b64encode(
            json.dumps(services_conf).encode()
        ).decode()

    oc("apply", "-n", namespace, "-f", "-", _in=json.dumps(secret), _silent=True)
    scale_down_up(namespace, "deployment", conf.GW_DEPLOYMENT)
