import logging

from fastapi import HTTPException, status, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositoryes.user import UserRepository
from app.repositoryes.user_session import UserSessionRepository
from app.core.security import create_access_token, create_refresh_token
from app.shemas.auth import TokenOut, UserLoginTelegramIn

log = logging.getLogger(__name__)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.repo_session = UserSessionRepository(db)

    async def login_telegram(self, user: UserLoginTelegramIn, response: Response):
        old_user = await self.repo.get_by_telegram(user.telegram_id)

        log.info('попытка создания пользователя')

        if not old_user:
            log.info('Пользователя нет')
            user = await self.repo.create(
                telegram_id=user.telegram_id,
                first_name=user.first_name,
                last_name=user.last_name,
                photo_url=user.photo_url,
                username=user.username,
            )
        else:
            user = old_user

        access_token = create_access_token(user.id, user.telegram_id,user.role)
        refresh_token = create_refresh_token(user.id)

        await self.repo_session.create(user.id,refresh_token)

        response.set_cookie(
            key="admin_token",
            value=access_token,  # Или сгенерируйте отдельный токен для админки
            httponly=True,  # Защита от XSS
            secure=False,  # Только HTTPS (в production)
        )
        return TokenOut(access_token=access_token, refresh_token=refresh_token)


    async def refresh(self, payload: dict, token) -> TokenOut:
        user_id = int(payload.get('sub'))

        user = await self.repo.get_with_sessions(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found")

        access_token = create_access_token(user.id, user.telegram_id,user.role)
        refresh_token = create_refresh_token(user.id)

        for i in user.sessions:
            if i.token == token:
                await self.repo_session.update(i,token=refresh_token)


        return TokenOut(access_token=access_token, refresh_token=refresh_token)
