from typing import Annotated

from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM
from app.schemas.post import PostPagination
from app.models.user import User
from app.db.database import AsyncSessionLocal
from app.exceptions.auth import InvalidCredentials
from app.services.token_service import get_token_from_header_or_cookie
from app.services.user_service import UserService
from app.repositories.user import UserRepository


PaginationDep = Annotated[PostPagination, Depends(PostPagination)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_user_repository(
    db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


async def get_current_user(token: str = Depends(get_token_from_header_or_cookie),
                           service: UserService = Depends(get_user_service)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise InvalidCredentials()

    user = await service.get_user(user_id=user_id)

    if user is None:
        raise InvalidCredentials()
    return user