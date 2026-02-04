from app.models.like import Like
from app.exceptions_handler import LikeNotFound, PostNotFound
from app.repositories.post import PostRepository
from app.repositories.like import LikeRepository


class LikeService:
    def __init__(self, repo: LikeRepository, post_repo: PostRepository):
        self.repo = repo
        self.post_repo = post_repo

    async def like_post(self, post_id: int, user_id: int) -> Like:
        post = await self.post_repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound()

        return await self.repo.add_like(user_id, post_id)

    async def unlike_post(self, post_id: int, user_id: int) -> bool:
        post = await self.post_repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound()

        deleted_id = await self.repo.delete_like(user_id, post_id)
        if deleted_id is None:
            raise LikeNotFound()

        return True