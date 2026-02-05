from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, or_

from app.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def  get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_login(self, login: str) -> User | None:
        stmt = select(User).filter(or_(User.username == login, User.email == login))
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_all_users(self) -> Sequence[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def user_exists(self, email: str, username: str) -> bool:
        stmt = select(
            exists().where(
                or_(User.username == username, User.email == email)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def create_user(self, **data) -> User:
        user = User(**data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user) -> None:
        await self.db.delete(user)
        await self.db.commit()