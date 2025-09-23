# tests/test_auth.py
import time

import pytest
import os
from dotenv import load_dotenv
import hmac
import hashlib

from app.core.config import load_config
config = load_config()

# Загрузка .env из папки tests
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

auth_date = round(time.time())

def get_auth_params(**overrides):
    params = {
        "id": os.getenv("AUTH_ID", "123456"),
        "first_name": os.getenv("AUTH_FIRST_NAME", "Test"),
        "last_name": os.getenv("AUTH_LAST_NAME", "User"),
        "username": os.getenv("AUTH_USERNAME", "testuser"),
        "photo_url": os.getenv("AUTH_PHOTO_URL", "http://test/photo.jpg"),
        "auth_date": auth_date,
    }
    params.update(overrides)
    return params

AUTH_URL = "/v1/auth/telegram"

print(config.MODE + 'ЭТО МОД КОНФИГА ДА')


data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(get_auth_params().items())])
secret_key = hashlib.sha256(config.bot.key.encode()).digest()
hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

def get_auth_params(**overrides):
    params = {
        "id": os.getenv("AUTH_ID", "123456"),
        "first_name": os.getenv("AUTH_FIRST_NAME", "Test"),
        "last_name": os.getenv("AUTH_LAST_NAME", "User"),
        "username": os.getenv("AUTH_USERNAME", "testuser"),
        "photo_url": os.getenv("AUTH_PHOTO_URL", "http://test/photo.jpg"),
        "auth_date": auth_date,
        "hash": hmac_hash
    }
    params.update(overrides)
    return params


@pytest.mark.asyncio
async def test_auth_success(client):
    response = client.get(AUTH_URL, params=get_auth_params())
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "token" in data or "access_token" in data

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "missing_field",
    ["id", "first_name", "last_name", "username", "photo_url", "auth_date", "hash"],
)
async def test_auth_missing_required_fields(client, missing_field):
    params = get_auth_params()
    params.pop(missing_field)
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400, 499)

@pytest.mark.asyncio
async def test_auth_invalid_hash(client):
    params = get_auth_params(hash="invalidhash")
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400, 499)

@pytest.mark.asyncio
async def test_auth_expired_auth_date(client):
    params = get_auth_params(auth_date="1000000000")  # Старое значение
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400, 499)

@pytest.mark.asyncio
async def test_auth_invalid_id(client):
    params = get_auth_params(id="notanumber")
    response = client.get(AUTH_URL, params=params)
    assert response.status_code in range(400, 499)