import pytest
from flask import Flask

from crcmocks.accounts_mgmt import MissingAuth, process_headers, BadBearerTokenValue

# Unit tests of the mocked accounts_mgmt endpoints


def test_process_headers():
    with pytest.raises(MissingAuth):
        process_headers({})

    with pytest.raises(BadBearerTokenValue):
        process_headers({"Authorization": "Barer de taco"})

    token = process_headers({"Authorization": "Bearer some_bearer"})
    assert token == "some_bearer"


def test_cluster_registrations():
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
