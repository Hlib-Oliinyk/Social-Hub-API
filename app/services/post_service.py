from typing import Sequence

from app.models.post import Post
from app.dependencies import PaginationDep
from app.exceptions_handler import PostNotFound, PostForbidden
from app.schemas.post import PostCreate
from app.repositories.post import PostRepository


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def get_post(self, post_id: int) -> Post:
        post = await self.repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound()
        return post

    async def get_posts(self, pagination: PaginationDep) -> Sequence[Post]:
        return await self.repo.get_posts(pagination)

    async def create_post(self, data: PostCreate, user_id: int) -> Post:
        post_dict = data.model_dump()
        post_dict["user_id"] = user_id
        return await self.repo.create_post(**post_dict)

    async def delete_post(self, user_id: int, post_id: int) -> bool:
        post = await self.get_post(post_id)
        if post.user_id != user_id:
            raise PostForbidden()
        return await self.repo.delete_post(post)

