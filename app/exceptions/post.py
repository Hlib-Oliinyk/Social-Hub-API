from app.exceptions import AppError

class PostNotFound(AppError):
    pass

class PostForbidden(AppError):
    pass