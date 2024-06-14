# pylint: disable=missing-function-docstring
from tests.assets.requests_validatiion_constants import METHOD_NOT_IMPLEMENTED


def test_login(client):
    response = client.post("my/login")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_logout(client):
    response = client.post("my/logout")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED
