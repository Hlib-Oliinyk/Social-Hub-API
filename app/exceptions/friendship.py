from app.exceptions.base import AppError

class FriendshipNotFound(AppError):
    pass

class FriendshipAlreadyExists(AppError):
    pass