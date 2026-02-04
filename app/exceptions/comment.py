from app.exceptions.base import AppError

class CommentForbidden(AppError):
    pass

class CommentNotFound(AppError):
    pass