from sqlalchemy import select
from app.models.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import PaginationDep
from app.exceptions_handler import PostNotFound, PostForbidden
from app.schemas.post import PostCreate


async def get_posts(db: AsyncSession, pagination: PaginationDep):
    stmt = select(Post).limit(pagination.limit).offset(pagination.offset)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)

    post = result.scalars().first()

    if not post:
        raise PostNotFound()
    return post


async def create_post(db: AsyncSession, data: PostCreate, user_id: int):
    post = Post(
        user_id = user_id,
        content = data.content,
    )

    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, user_id: int, post_id: int):
    post = await get_post(db, post_id)

    if post.user_id != user_id:
        raise PostForbidden()

    await db.delete(post)
    await db.commit()
    return True

