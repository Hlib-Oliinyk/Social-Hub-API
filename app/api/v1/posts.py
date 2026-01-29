from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.schemas.post import PostResponse
import app.services.post_service as post_service
from app.dependencies import PaginationDep
from app.models.user import User
from app.schemas.post import PostCreate

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", response_model=list[PostResponse])
async def get_posts(pagination: PaginationDep, db: AsyncSession = Depends(get_db)):
    return await post_service.get_posts(db, pagination)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await post_service.get_post(db, post_id)


@router.post("")
async def create_post(data: PostCreate, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    return await post_service.create_post(db, data, current_user.id)


@router.delete("/{post_id}")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    return await post_service.delete_post(db, current_user.id, post_id)