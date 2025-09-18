from fastapi import Request, HTTPException, APIRouter, status, Depends,Response
import httpx

from app.api.depencies.services import get_auth_service
from app.services.auth import AuthService
from app.shemas.auth import UserAuthTelegramIn
from app.utils.telegram import check_telegram_auth

from app.core.config import load_config

config = load_config()

BOT_TOKEN = config.bot.key

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/telegram", status_code=status.HTTP_201_CREATED, summary="Login via Telegram")
async def login_telegram(
    user: UserAuthTelegramIn,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    print(user.dict())
    if not check_telegram_auth(user.dict(), BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid Telegram data")
    return await service.login_telegram(user, response)

API_URL = "http://127.0.0.1/v1/auth/telegram"

@router.get("/telegram")
async def telegram_callback(request: Request):
    data = dict(request.query_params)

    if not data:
        raise HTTPException(status_code=400, detail="No data from Telegram")

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=data)

    return response.json()


# @router.get("/telegram")
# async def telegram_auth(request: Request):
#     data = dict(request.query_params)
#
#     if not check_telegram_auth(data, BOT_TOKEN):
#         raise HTTPException(status_code=403, detail="Invalid Telegram data")
#
#     # Здесь можно создать JWT/сессию
#     return {
#         "ok": True,
#         "id": data["id"],
#         "username": data.get("username"),
#         "first_name": data.get("first_name"),
#         "first_name1": data.get("photo_url"),
#         'another': list(data.keys())
#     }


