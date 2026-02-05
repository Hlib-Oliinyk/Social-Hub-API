from typing import Sequence

from app.exceptions.friendship import FriendshipAlreadyExists
from app.models import Friendship
from app.schemas import (
    FriendshipCreate,
    FriendResponse
)
from app.exceptions.user import UserNotFound
from app.exceptions.friendship import FriendshipNotFound
from app.repositories import FriendshipRepository, UserRepository


class FriendshipService:
    def __init__(self, repo: FriendshipRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    async def get_friends(self, user_id: int):
        friends = await self.repo.get_friends_with_names(user_id)
        return [FriendResponse.model_validate(f) for f in friends]

    async def get_friendship(self, friendship_id: int) -> Friendship:
        friendship = await self.repo.get_friendship(friendship_id)
        if friendship is None:
            raise FriendshipNotFound()
        return friendship

    async def send_friendship(self, user_id: int, data: FriendshipCreate) -> Friendship:
        addressee = await self.user_repo.get_by_id(user_id)
        if addressee is None:
            raise UserNotFound()

        if await self.repo.friendship_exists(user_id, data.addressee_id):
            raise FriendshipAlreadyExists()

        friendship_dict = data.model_dump()
        friendship_dict["requester_id"] = user_id

        return await self.repo.send_friendship(**friendship_dict)

    async def accept_friendship_request(self, friendship_id: int) -> Friendship:
        friendship = await self.repo.get_friendship(friendship_id)
        if friendship is None:
            raise FriendshipNotFound()
        return await self.repo.accept_request(friendship)

    async def reject_friendship_request(self, friendship_id: int) -> Friendship:
        friendship = await self.repo.get_friendship(friendship_id)
        if friendship is None:
            raise FriendshipNotFound()
        return await self.repo.reject_request(friendship)

    async def get_friendship_requests(self, user_id: int) -> Sequence[Friendship]:
        return await self.repo.get_requests(user_id)

    async def delete_friendship(self, user_id: int, friend_id: int) -> bool:
        is_deleted = await self.repo.delete_friendship(user_id, friend_id)
        if not is_deleted:
            raise FriendshipNotFound()
        return is_deleted