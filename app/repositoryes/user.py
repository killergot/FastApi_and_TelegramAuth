from typing import Optional
import logging

from sqlalchemy import select

from uuid import UUID

from sqlalchemy.orm import selectinload

from app.database.models.auth import User, UserSession
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.users import UserUpdateIn

log = logging.getLogger(__name__)

class UserRepository(TemplateRepository):
    async def get_all(self):
        data = select(User)
        users = await self.db.execute(data)
        return users.scalars().all()

    async def get_with_sessions(self,user_id:int) -> Optional[User]:
        data = (select(User).
        where(User.id == user_id).
        options(
                selectinload(User.sessions)
            ))
        users = await self.db.execute(data)
        user = users.scalars().first()
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        data = select(User).where(User.email == email)
        user = await self.db.execute(data)
        return user.scalars().first()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_by_telegram(self, telegram_id: int) -> Optional[User]:
        data = select(User).where(User.telegram_id == telegram_id)
        user = await self.db.execute(data)
        return user.scalars().first()

    async def create(self,telegram_id: int,
                     first_name: str,
                     last_name: str,
                     photo_url: str,
                     username: str,
                     email: Optional[str] = None,
                     password: Optional[str] = None,
                     role: int = 0) -> User:
        new_user = User(email=email,
                        password=password,
                        role=role,
                        telegram_id=telegram_id,
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        photo_url=photo_url)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    @except_handler
    async def update(self,user_id: int, new_user: UserUpdateIn) -> User:
        user = await self.get_by_id(user_id)
        if new_user.telegram_id:
            user.telegram_id = new_user.telegram_id
        if new_user.first_name:
            user.first_name = new_user.first_name
        if new_user.last_name:
            user.last_name = new_user.last_name
        if new_user.username:
            user.username = new_user.username
        if new_user.email:
            user.email = new_user.email
        if new_user.photo_url:
            user.photo_url = new_user.photo_url


        await self.db.commit()
        await self.db.refresh(user)
        return user


    @except_handler
    async def delete(self, user_id: int) -> bool:
        await self.db.delete(await self.get_by_id(user_id))
        await self.db.commit()
        return True