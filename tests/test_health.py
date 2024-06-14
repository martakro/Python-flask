# pylint: disable=missing-function-docstring


def test_base(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"msg": "Hello World!"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"msg": "OK"}
