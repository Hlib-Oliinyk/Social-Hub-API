from fastapi import Request
from fastapi.params import Depends
from app.db.database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.services.user_service import get_user
from app.schemas.post import PostPagination
from app.models.user import User
from app.exceptions.auth import *
from typing import Annotated

PaginationDep = Annotated[PostPagination, Depends(PostPagination)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


async def get_token_from_header_or_cookie(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]

    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token

    raise InvalidCredentials()


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token_from_header_or_cookie)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise InvalidCredentials()

    user = await get_user(db, user_id=user_id)

    if user is None:
        raise InvalidCredentials()

    return user