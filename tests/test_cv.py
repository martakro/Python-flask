# pylint: disable=missing-function-docstring

from tests.assets.requests_validatiion_constants import (
    METHOD_NOT_IMPLEMENTED,
    NOT_FOUND,
)


def test_get_my_cv(client):
    response = client.get("/my")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_update_cv(client):
    response = client.patch("/my")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_delete_cv(client):
    response = client.delete("/my")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_incorrect_uri(client):
    response = client.get("/whatever")
    assert response.status_code == 404
    assert response.json == NOT_FOUND
