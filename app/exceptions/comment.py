from app.exceptions import AppError

class CommentForbidden(AppError):
    pass

class CommentNotFound(AppError):
    pass