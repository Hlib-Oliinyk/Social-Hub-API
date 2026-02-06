from typing import Sequence

from app.exceptions import PostNotFound
from app.schemas import CommentCreate
from app.models import Comment
from app.exceptions_handler import CommentForbidden, CommentNotFound
from app.repositories import CommentRepository, PostRepository


class CommentService:
    def __init__(self, repo: CommentRepository, post_repo: PostRepository):
        self.repo = repo
        self.post_repo = post_repo

    async def get_comment(self, comment_id: int) -> Comment:
        comment = await self.repo.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFound()
        return comment

    async def get_post_comments(self, post_id: int) -> Sequence[Comment]:
        post = await self.post_repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound()
        return await self.repo.get_comments_by_post(post_id)

    async def add_comment(self, post_id: int, user_id: int, data: CommentCreate) -> Comment:
        post = await self.post_repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound()

        return await self.repo.create_comment(
            **data.model_dump(),
            post_id = post_id,
            user_id = user_id
        )

    async def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = await self.repo.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFound()

        if comment.user_id != user_id:
            raise CommentForbidden()

        await self.repo.delete_comment(comment)
        return True