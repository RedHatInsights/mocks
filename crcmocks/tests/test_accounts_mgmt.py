import pytest
from flask import Flask
from crcmocks.accounts_mgmt import accounts_mgmt
from crcmocks.accounts_mgmt import MissingAuth, process_headers, BadBearerTokenValue

# Unit tests of the mocked accounts_mgmt endpoints
from crcmocks.db import upsert_org

app = Flask(__name__)
app.register_blueprint(accounts_mgmt, url_prefix="")


def test_process_headers():
    with pytest.raises(MissingAuth):
        process_headers({})

    with pytest.raises(BadBearerTokenValue):
        process_headers({"Authorization": "Barer de taco"})

    token = process_headers({"Authorization": "Bearer some_bearer"})
    assert token == "some_bearer"


def test_cluster_registrations():
    """ Confirm that we can 'register' a cluster to an account. """
    app = Flask(__name__)
    from crcmocks.accounts_mgmt import accounts_mgmt

    app.register_blueprint(accounts_mgmt, url_prefix="")
    resource = "/api/accounts_mgmt/v1/cluster_registrations"
    with app.test_client() as client:
        response = client.get(resource)
        assert response.status_code == 405

        response = client.post(resource)
        assert response.status_code == 401
        sample_body = {}
        response = client.post(
            resource, data=sample_body, headers={"Authorization": "Bearer sometoken"}
        )
        assert response.status_code == 400

        valid_body = {"cluster_id": "12345", "authorization_token": "sometoken"}
        response = client.post(
            resource, data=valid_body, headers={"Authorization": "Bearer sometoken"}
        )
        assert response.status_code == 200
        assert response.json["account_id"]
        assert response.json["authorization_token"]
        assert response.json["cluster_id"]
        assert response.json["expires_at"]


def test_get_account():
    """ Confirm the endpoint gives us an organization id. """
    some_account = "12345"
    resource = f"/api/accounts_mgmt/v1/accounts/{some_account}"
    headers = {"Authorization": "Bearer potatosalad"}
    with app.test_client() as client:
        response = client.get(resource, headers=headers)
        items = response.json["items"]
        assert items[0]["organization"]["id"]


def test_get_organization():
    some_org_id = "12345"
    upsert_org(org_id="12345", ebs_account="54321", external_id="external_12345")
    resource = f"/api/accounts_mgmt/v1/organizations/{some_org_id}"
    headers = {"Authorization": "Bearer macaroni"}
    with app.test_client() as client:
        response = client.get(resource, headers=headers)
        assert response.status_code == 200
        assert response.json["ebs_account_id"] == "54321"
        assert response.json["external_id"] == "external_12345"
