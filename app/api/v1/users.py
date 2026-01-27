from fastapi import APIRouter
from fastapi.params import Depends
from app.dependencies import get_current_user, get_db
from app.schemas.user import UserResponse
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
import app.services.user_service as user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user( user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user(db, user_id)


@router.delete("/me")
async def delete_user(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_service.delete_user(db, current_user.id)