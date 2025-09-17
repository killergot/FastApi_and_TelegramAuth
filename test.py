from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import hashlib
import hmac
import time

BOT_TOKEN = "8351814758:AAHuwOpyizho9z-O1ZGLd5zmvYnqP4dGX_k"  # возьмите у @BotFather

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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

    return True

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth/telegram")
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
