from app.exceptions.user import UserAlreadyExists, UserNotFound
from app.exceptions.auth import InvalidCredentials
from app.exceptions.friendship import FriendshipNotFound, FriendshipAlreadyExists
from app.exceptions.post import PostForbidden, PostNotFound
from app.exceptions.comment import CommentForbidden, CommentNotFound
from app.exceptions.like import LikeNotFound, PostAlreadyLiked