from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.schemas.post import PostResponse, PostCreate
from app.dependencies import PaginationDep
from app.models.user import User
from app.schemas.comment import CommentResponse, CommentCreate
from app.schemas.like import LikeResponse
from app.dependencies import get_post_service
from app.services.post_service import PostService

import app.services.comment_service as comment_service
import app.services.like_service as like_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", response_model=list[PostResponse])
async def get_posts(
    pagination: PaginationDep,
    service: PostService = Depends(get_post_service)
):
    return await service.get_posts(pagination)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    service: PostService = Depends(get_post_service)
):
    return await service.get_post(post_id)


@router.post("")
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    return await service.create_post(data, current_user.id)


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    return await service.delete_post(current_user.id, post_id)


@router.get("/{post_id}/comments", response_model=list[CommentResponse])
async def get_post_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    post_service: PostService = Depends(get_post_service)
):
    return await comment_service.get_post_comments(db, post_id, post_service)


@router.post("/{post_id}/comments")
async def add_comment(
    post_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    post_service: PostService = Depends(get_post_service)
):
    return await comment_service.add_comment(db, data, current_user.id, post_id, post_service)


@router.post("/{post_id}/like", response_model=LikeResponse)
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    post_service: PostService = Depends(get_post_service)
):
    return await like_service.like_post(db, post_id, current_user.id, post_service)


@router.delete("/{post_id}/like")
async def unlike_post(
    post_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    post_service: PostService = Depends(get_post_service)
):
    return await like_service.unlike_post(db, post_id, current_user.id, post_service)