from fastapi import  Depends


from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.db import get_db

from app.services.auth import AuthService
from app.services.user import UserService

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)