from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import app.services.friendship_service as friendship_service
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.friendship import FriendshipResponse, FriendshipCreate, FriendResponse, FriendshipUpdate

router = APIRouter(prefix="/friends", tags=["Friends"])

@router.get("", response_model=list[FriendResponse])
async def get_friends(current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await friendship_service.get_friends(db, current_user.id)


@router.get("/requests", response_model=list[FriendshipResponse])
async def get_friendship_requests(current_user: User = Depends(get_current_user),
                                  db: AsyncSession = Depends(get_db)):
    return await friendship_service.get_friendship_requests(db, current_user.id)


@router.post("/{user_id}")
async def send_friendship_request(data: FriendshipCreate, current_user: User = Depends(get_current_user),
                                  db: AsyncSession = Depends(get_db)):
    return await friendship_service.send_friendship(db, data, current_user.id)


@router.post("/{user_id}/accept")
async def accept_friendship_request(friendship_id: int, data: FriendshipUpdate,
                                    db: AsyncSession = Depends(get_db)):
    return await friendship_service.accept_friendship_request(db, friendship_id, data)


@router.post("/{user_id}/reject")
async def reject_friendship_request(friendship_id: int, data: FriendshipUpdate,
                                    db: AsyncSession = Depends(get_db)):
    return await friendship_service.reject_friendship_request(db, friendship_id, data)


@router.delete("/{user_id}")
async def delete_friendship(friend_id: int, current_user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    return await friendship_service.delete_friendship(db, friend_id, current_user.id)