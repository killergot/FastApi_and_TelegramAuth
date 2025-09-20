import pytest
from fastapi.testclient import TestClient

from app.main import app  # Импортируйте ваш FastAPI app

client = TestClient(app)

AUTH_URL = "/v1/auth/telegram"

def get_auth_params(**overrides):
    params = {
        "id": "123",
        "first_name": "name",
        "last_name": "lastname",
        "username": "username",
        "photo_url": "http://example.com/example.jpg",
        "auth_date": "222222222",
        "hash": "test_hash",
    }
    params.update(overrides)
    return params

def test_auth_success():
    response = client.get(AUTH_URL, params=get_auth_params())
    assert response.status_code == 200
    data = response.json()
    assert "token" in data or "access_token" in data

@pytest.mark.parametrize("missing_field", [
    "id", "first_name", "last_name", "username", "photo_url", "auth_date", "hash"
])
def test_auth_missing_required_fields(missing_field):
    params = get_auth_params()
    params.pop(missing_field)
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400,499)

def test_auth_invalid_hash():
    params = get_auth_params(hash="invalidhash")
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400,499)

def test_auth_expired_auth_date():
    params = get_auth_params(auth_date="1000000000")  # Старое значение
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400,499)

def test_auth_invalid_id():
    params = get_auth_params(id="notanumber")
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400,499)