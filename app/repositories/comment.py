from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, commend_id: int) -> Comment | None:
        stmt = select(Comment).where(Comment.id == commend_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_comments_by_post(self, post_id: int) -> Sequence[Comment]:
        stmt = select(Comment).where(Comment.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_comment(self, **data) -> Comment:
        comment = Comment(**data)
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete_comment(self, comment) -> bool:
        await self.db.delete(comment)
        await self.db.commit()
        return True
