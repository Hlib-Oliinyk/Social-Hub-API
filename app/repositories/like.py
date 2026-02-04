from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.like import Like
from app.exceptions_handler import PostAlreadyLiked


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_like(self, user_id: int, post_id: int) -> Like:
        like = Like(user_id=user_id, post_id=post_id)
        self.db.add(like)

        try:
            await self.db.commit()
            await self.db.refresh(like)
            return like
        except IntegrityError:
            await self.db.rollback()
            raise PostAlreadyLiked()

    async def delete_like(self, user_id: int, post_id: int) -> int | None:
        stmt = delete(Like).where(
            Like.user_id == user_id,
            Like.post_id == post_id
        ).returning(Like.id)

        result = await self.db.execute(stmt)
        deleted_id = result.scalar_one_or_none()

        if deleted_id:
            await self.db.commit()

        return deleted_id