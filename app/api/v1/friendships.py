from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies import (
    get_current_user,
    get_friendship_service
)
from app.models import User
from app.schemas import FriendshipResponse, FriendshipCreate, FriendResponse
from app.services import FriendshipService


router = APIRouter(prefix="/friends", tags=["Friends"])

@router.get("", response_model=list[FriendResponse])
async def get_friends(
    current_user: User = Depends(get_current_user),
    service: FriendshipService = Depends(get_friendship_service)
):
    return await service.get_friends(current_user.id)


@router.get("/requests", response_model=list[FriendshipResponse])
async def get_friendship_requests(
    current_user: User = Depends(get_current_user),
    service: FriendshipService = Depends(get_friendship_service)
):
    return await service.get_friendship_requests(current_user.id)


@router.post("/{user_id}")
async def send_friendship_request(
    data: FriendshipCreate,
    current_user: User = Depends(get_current_user),
    service: FriendshipService = Depends(get_friendship_service)
):
    return await service.send_friendship(current_user.id, data)


@router.post("/{user_id}/accept")
async def accept_friendship_request(
    friendship_id: int,
    service: FriendshipService = Depends(get_friendship_service)
):
    return await service.accept_friendship_request(friendship_id)


@router.post("/{user_id}/reject")
async def reject_friendship_request(
    friendship_id: int,
    service: FriendshipService = Depends(get_friendship_service)
):
    return await service.reject_friendship_request(friendship_id)


@router.delete("/{user_id}")
async def delete_friendship(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    service: FriendshipService = Depends(get_friendship_service)
):
    return await service.delete_friendship(current_user.id, friend_id)