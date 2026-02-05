from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies import get_current_user, get_user_service
from app.schemas import UserResponse
from app.models import User
from app.services import UserService


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user(user_id)


@router.delete("/me")
async def delete_user(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return await service.delete_user(current_user.id)