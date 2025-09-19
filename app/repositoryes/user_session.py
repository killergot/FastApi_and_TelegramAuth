from typing import Optional
import logging

from sqlalchemy import select

from uuid import UUID
from app.database.models.auth import UserSession
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class UserSessionRepository(TemplateRepository):
    async def get_all(self) -> list[UserSession]:
        data = select(UserSession)
        users = await self.db.execute(data)
        return users.scalars().all()

    async def get(self, session: UUID) -> Optional[UserSession]:
        return await self.db.get(UserSession, session)

    async def create(self,user_id: int,
                     token: str) -> UserSession:
        new_UserSession = UserSession(
            user_id=user_id,
            token=token,
        )
        self.db.add(new_UserSession)
        await self.db.commit()
        await self.db.refresh(new_UserSession)

        return new_UserSession

    @except_handler
    async def update(self, session: UserSession,
                     token: str) -> UserSession:
        session.token = token
        await self.db.commit()
        await self.db.refresh(session)
        return session


    @except_handler
    async def delete(self, session: UserSession) -> bool:
        await self.db.delete(session)
        await self.db.commit()
        return True