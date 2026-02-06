from .base import AppError

class PostAlreadyLiked(AppError):
    pass

class LikeNotFound(AppError):
    pass