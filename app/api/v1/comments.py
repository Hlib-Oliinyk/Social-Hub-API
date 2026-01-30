from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import app.services.comment_service as comment_service
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/delete")
async def delete_comment(comment_id: int, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    return await comment_service.delete_comment(db, comment_id, current_user.id)

