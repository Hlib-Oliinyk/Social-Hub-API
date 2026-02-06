from .base import AppError

class UserNotFound(AppError):
    pass

class UserAlreadyExists(AppError):
    pass