from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.like import Like
from app.exceptions_handler import PostAlreadyLiked, LikeNotFound
from app.services.post_service import PostService


async def like_post(db: AsyncSession,post_id: int,user_id: int,post_service: PostService):
    await post_service.get_post(post_id)

    like = Like(
        user_id = user_id,
        post_id = post_id
    )
    db.add(like)

    try:
        await db.commit()
        await db.refresh(like)
    except IntegrityError:
        await db.rollback()
        raise PostAlreadyLiked()
    return like


async def unlike_post(db: AsyncSession, post_id: int, user_id: int, post_service: PostService):
    await post_service.get_post(post_id)

    stmt = delete(Like).where(Like.user_id == user_id, Like.post_id == post_id).returning(Like.id)
    result = await db.execute(stmt)
    deleted_like = result.scalar_one_or_none()
    await db.commit()

    if deleted_like is None:
        raise LikeNotFound
    return True