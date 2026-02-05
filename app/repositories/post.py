from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Post


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> Post | None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_posts(self, limit, offset) -> Sequence[Post]:
        stmt = select(Post).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_post(self, **data) -> Post:
        post = Post(**data)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def delete_post(self, post) -> bool:
        await self.db.delete(post)
        await self.db.commit()
        return True