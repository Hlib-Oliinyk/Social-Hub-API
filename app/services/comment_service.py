from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.comment import CommentCreate
from app.models.comment import Comment
from app.services.post_service import get_post
from app.exceptions_handler import CommentForbidden, CommentNotFound


async def get_comment(db: AsyncSession, comment_id: int):
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(stmt)

    comment = result.scalars().first()

    if not comment:
        raise CommentNotFound()
    return comment


async def get_post_comments(db: AsyncSession, post_id: int):
    post = await get_post(db, post_id)

    stmt = select(Comment).where(Comment.post_id == post.id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def add_comment(db: AsyncSession, data: CommentCreate, user_id: int):

    await get_post(db, data.post_id)

    comment = Comment(
        post_id = data.post_id,
        user_id = user_id,
        content = data.content
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment_id: int, user_id: int):
    comment = await get_comment(db, comment_id)

    if comment.user_id != user_id:
        raise CommentForbidden()

    await db.delete(comment)
    await db.commit()
    return True