from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, RowMapping, delete

from app.models import Post, User, Like


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int):
        stmt = (
            select
                (
                Post.id,
                User.username,
                User.id.label("user_id"),
                Post.content,
                Post.created_at,
                func.count(Like.id).label("likes_count")
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(Like, Like.post_id == Post.id)
            .where(Post.id == post_id)
            .group_by(Post.id, User.username, User.id)
        )
        result = await self.db.execute(stmt)
        return result.mappings().first()

    async def get_posts(self, limit, offset) -> Sequence[RowMapping]:
        stmt = (
            select
            (
                Post.id,
                User.username,
                Post.content,
                Post.created_at,
                func.count(Like.id).label("likes_count")
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(Like, Like.post_id == Post.id)
            .group_by(Post.id, User.username)
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def create_post(self, **data) -> Post:
        post = Post(**data)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def delete_post(self, post_id: int) -> bool:
        stmt = delete(Post).where(Post.id == post_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True