import pytest

from app import add, app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_function():
    assert add(2, 3) == 5


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_version_defaults_to_dev(client, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert client.get("/version").get_json() == {"version": "dev"}


def test_add_endpoint(client):
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 5.0}


def test_add_endpoint_rejects_bad_input(client):
    response = client.get("/add?a=two&b=3")
    assert response.status_code == 400
