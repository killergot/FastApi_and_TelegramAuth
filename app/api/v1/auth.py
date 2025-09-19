import logging

from fastapi import Request, HTTPException, APIRouter, status, Depends,Response
import httpx

from app.api.depencies.services import get_auth_service
from app.services.auth import AuthService
from app.shemas.auth import UserLoginTelegramIn
from app.utils.telegram import check_telegram_auth

from app.core.config import load_config

config = load_config()

BOT_TOKEN = config.bot.key

router = APIRouter(prefix="/auth", tags=["auth"])
log = logging.getLogger(__name__)


@router.get("/telegram", summary="Login via Telegram")
async def telegram_login(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    # Получаем данные, которые Telegram передаёт в query
    data = dict(request.query_params)

    if not data:
        raise HTTPException(status_code=400, detail="No data from Telegram")

    # Проверяем подпись от Telegram
    if not check_telegram_auth(data, BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid Telegram data")

    log.info(f"Login via Telegram {data['id']}  {data['username']}")

    # Преобразуем query-параметры в Pydantic-модель
    data['telegram_id'] = data.pop("id")

    try:
        user = UserLoginTelegramIn(**data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid user data: {e}")

    # Сразу вызываем сервис логина
    return await service.login_telegram(user, response)

