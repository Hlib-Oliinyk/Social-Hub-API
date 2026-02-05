from .comment import CommentRepository
from .post import PostRepository
from .like import LikeRepository
from .user import UserRepository
from .friendship import FriendshipRepository

__all__ = [
    "CommentRepository",
    "PostRepository",
    "LikeRepository",
    "UserRepository",
    "FriendshipRepository"
]