from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies import get_current_user, get_comment_service
from app.models.user import User
from app.services import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/delete")
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service)
):
    return await service.delete_comment(comment_id, current_user.id)

