from fastapi import Request, HTTPException, APIRouter
from app.utils.telegram import check_telegram_auth

from app.core.config import load_config

config = load_config()


BOT_TOKEN = config.bot.key

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/telegram")
async def telegram_auth(request: Request):
    data = dict(request.query_params)

    if not check_telegram_auth(data, BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid Telegram data")

    # Здесь можно создать JWT/сессию
    return {
        "ok": True,
        "id": data["id"],
        "username": data.get("username"),
        "first_name": data.get("first_name"),
    }
