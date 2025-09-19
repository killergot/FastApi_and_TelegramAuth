from uuid import UUID

from fastapi import  HTTPException, status

from app.database.models.auth import UserSession
from app.repositoryes.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositoryes.user_session import UserSessionRepository
from app.shemas.users import UserOut, UserUpdateIn
from app.database import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.repo_session = UserSessionRepository(db)

    async def _get(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    async def get_by_email(self, email: str) -> UserOut:
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return UserOut.model_validate(user)

    async def get_by_telegram(self, telegram_id: int) -> UserOut:
        user = await self.repo.get_by_telegram(telegram_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return UserOut.model_validate(user)

    async def get_by_id(self, user_id: int) -> UserOut:
        user = await self._get(user_id)
        return UserOut.model_validate(user)

    async def get_all(self) -> list[UserOut]:
        users = await self.repo.get_all()
        return users

    async def update(self, user: UserOut, update_data: UserUpdateIn) -> UserOut:
        user = await self.repo.update(user.id, update_data)
        return UserOut.model_validate(user)

    async def del_by_id(self, id: int) -> None:
        _ = await self._get(id)
        if not await self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_500_NOT_FOUND,
                                detail="Error deleting user")

    async def get_sessions(self, user_id: int) -> list[UserSession]:
        sessions = await self.repo.get_with_sessions(user_id)
        if not sessions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return sessions.sessions

    async def delete_session(self, session_id: UUID, user_id: int) -> None:
        session = await self.repo_session.get(session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Session not found")
        if not await self.repo_session.delete(session):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Error deleting session")

