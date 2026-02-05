from .auth import router as auth_router
from .users import router as users_router
from .friendships import router as friendships_router
from .posts import router as posts_router
from .comments import router as comments_router

__all__ = [
    "auth_router",
    "users_router",
    "friendships_router",
    "posts_router",
    "comments_router"
]