from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, and_, tuple_, delete

from app.models import Friendship, FriendStatus, User


class FriendshipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_friends_with_names(self, user_id: int):
        s1 = (
            select(User.id, User.username)
            .join(Friendship, User.id == Friendship.addressee_id)
            .where(
                Friendship.requester_id == user_id,
                Friendship.status == FriendStatus.accepted
            )
        )

        s2 = (
            select(User.id, User.username)
            .join(Friendship, User.id == Friendship.requester_id)
            .where(
                Friendship.addressee_id == user_id,
                Friendship.status == FriendStatus.accepted
            )
        )

        stmt = s1.union(s2)
        result = await self.db.execute(stmt)
        return result.all()

    async def get_friendship(self, friendship_id: int) -> Friendship | None:
        stmt = select(Friendship).where(Friendship.id == friendship_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def friendship_exists(self, user1_id: int, user2_id: int) -> bool:
        ids = (user1_id, user2_id)
        reversed_ids = (user2_id, user1_id)

        stmt = select(exists().where(
           and_(
               tuple_(Friendship.requester_id, Friendship.addressee_id).in_([ids, reversed_ids]),
               Friendship.status.in_([FriendStatus.accepted, FriendStatus.pending])
           )
        ))

        result = await self.db.execute(stmt)
        return result.scalar()

    async def send_friendship(self, **data) -> Friendship:
        friendship = Friendship(**data)
        self.db.add(friendship)
        await self.db.commit()
        await self.db.refresh(friendship)
        return friendship

    async def accept_request(self, friendship) -> Friendship:
        friendship.status = FriendStatus.accepted
        await self.db.commit()
        await self.db.refresh(friendship)
        return friendship

    async def reject_request(self, friendship) -> Friendship:
        friendship.status = FriendStatus.rejected
        await self.db.commit()
        await self.db.refresh(friendship)
        return friendship

    async def get_requests(self, user_id: int) -> Sequence[Friendship]:
        stmt = select(Friendship).where(
            Friendship.addressee_id == user_id,
            Friendship.status == FriendStatus.pending
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete_friendship(self, user1_id: int, user2_id: int) -> bool:
        pairs = [(user1_id, user2_id), (user2_id, user1_id)]

        stmt = (
            delete(Friendship)
            .where(
                tuple_(Friendship.addressee_id, Friendship.requester_id).in_(pairs),
                Friendship.status == FriendStatus.accepted
            )
            .returning(Friendship.id)
        )

        result = await self.db.execute(stmt)
        if result.scalar_one_or_none():
            await self.db.commit()
            return True
        return False