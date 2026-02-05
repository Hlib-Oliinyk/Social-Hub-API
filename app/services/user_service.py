from typing import Sequence

from app.core.security import hash_password, verify_password
from app.models import User
from app.schemas import UserCreate
from app.exceptions.user import UserNotFound, UserAlreadyExists
from app.repositories import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound()
        return user

    async def get_all_users(self) -> Sequence[User]:
        return await self.repo.get_all_users()

    async def create_user(self, data: UserCreate) -> User:
        exists = await self.repo.user_exists(data.email, data.username)
        if exists:
            raise UserAlreadyExists()

        user_dict = data.model_dump()
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))

        return await self.repo.create_user(**user_dict)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        await self.repo.delete_user(user)
        return True

    async def authenticate_user(self, login: str, password: str) -> User | None:
        user = await self.repo.get_by_login(login)
        if user is None or not verify_password(password, user.hashed_password):
            return None
        return user