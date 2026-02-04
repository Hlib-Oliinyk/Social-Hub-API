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
from app.services import (
    UserService,
    PostService,
    CommentService,
    LikeService
)
from app.repositories import (
    UserRepository,
    PostRepository,
    CommentRepository,
    LikeRepository
)


PaginationDep = Annotated[PostPagination, Depends(PostPagination)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_post_repository(db: AsyncSession = Depends(get_db)) -> PostRepository:
    return PostRepository(db)


def get_post_service(repo: PostRepository = Depends(get_post_repository)) -> PostService:
    return PostService(repo)


def get_comment_repository(db: AsyncSession = Depends(get_db)) -> CommentRepository:
    return CommentRepository(db)


def get_comment_service(
    comment_repo: CommentRepository = Depends(get_comment_repository),
    post_repo: PostRepository = Depends(get_post_repository)
) -> CommentService:
    return CommentService(comment_repo, post_repo)


def get_like_repository(db: AsyncSession = Depends(get_db)) -> LikeRepository:
    return LikeRepository(db)


def get_like_service(
    like_repo: LikeRepository = Depends(get_like_repository),
    post_repo: PostRepository = Depends(get_post_repository)
) -> LikeService:
    return LikeService(like_repo, post_repo)


async def get_current_user(
    token: str = Depends(get_token_from_header_or_cookie),
    service: UserService = Depends(get_user_service)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise InvalidCredentials()

    user = await service.get_user(user_id=user_id)
    if user is None:
        raise InvalidCredentials()
    return user