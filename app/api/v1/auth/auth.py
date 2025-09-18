from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import hashlib
import hmac
import time

BOT_TOKEN = "8351814758:AAH5h6fUO1rGMpSNN_uKEiMT3kdWSOASVr0"  # возьмите у @BotFather

router = APIRouter(prefix="/auth", tags=["auth"])

def check_telegram_auth(data: dict) -> bool:
    """Проверка подлинности данных от Telegram"""
    auth_data = data.copy()
    hash_ = auth_data.pop("hash")

    # Сортируем ключи и собираем строку
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(auth_data.items())])

    # Вычисляем HMAC-SHA256
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hmac_hash != hash_:
        return False

    # Проверка свежести (1 день)
    if time.time() - int(auth_data["auth_date"]) > 86400:
        return False

    print('Все проходит успешно')

    return True

@router.get("/telegram")
async def telegram_auth(request: Request):
    data = dict(request.query_params)

    if not check_telegram_auth(data):
        raise HTTPException(status_code=403, detail="Invalid Telegram data")

    # Здесь можно создать JWT/сессию
    return {
        "ok": True,
        "id": data["id"],
        "username": data.get("username"),
        "first_name": data.get("first_name"),
    }
