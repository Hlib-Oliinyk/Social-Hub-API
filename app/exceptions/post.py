from app.exceptions.base import AppError

class PostNotFound(AppError):
    pass

class PostForbidden(AppError):
    pass