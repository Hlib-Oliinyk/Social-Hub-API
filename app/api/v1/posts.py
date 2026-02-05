from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies import (
    get_current_user,
    get_comment_service,
    get_like_service
)
from app.schemas import (
    PostResponse,
    PostCreate,
    CommentResponse,
    CommentCreate,
    LikeResponse
)
from app.dependencies import PaginationDep, get_post_service
from app.models import User
from app.services import (
    PostService,
    CommentService,
    LikeService
)


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
    service: CommentService = Depends(get_comment_service)
):
    return await service.get_post_comments(post_id)


@router.post("/{post_id}/comments")
async def add_comment(
    post_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service)
):
    return await service.add_comment(post_id, current_user.id, data)


@router.post("/{post_id}/like", response_model=LikeResponse)
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: LikeService = Depends(get_like_service)
):
    return await service.like_post(post_id, current_user.id)


@router.delete("/{post_id}/like")
async def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: LikeService = Depends(get_like_service)
):
    return await service.unlike_post(post_id, current_user.id)