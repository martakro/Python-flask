# pylint: disable=missing-function-docstring
from tests.assets.requests_validatiion_constants import METHOD_NOT_IMPLEMENTED

USER_ID = 1


def test_get_users(client):
    response = client.get("/admin/users")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_create_user(client):
    response = client.post("/admin/users")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_get_user_data(client):
    response = client.get(f"/admin/users/{USER_ID}")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_update_user_data(client):
    response = client.patch(f"/admin/users/{USER_ID}")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_delete_user(client):
    response = client.delete(f"/admin/users/{USER_ID}")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED
