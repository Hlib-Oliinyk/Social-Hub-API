from sqlalchemy import select, or_, exists, and_
from app.exceptions import FriendshipAlreadyExists
from app.models.friendship import Friendship
from app.schemas.friendship import FriendshipCreate, FriendStatus, FriendshipUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_user
from app.exceptions.user import UserNotFound
from app.exceptions.friendship import FriendshipNotFound


async def get_friendships(db: AsyncSession, user_id: int):
    stmt = select(Friendship).filter(
        or_(
            Friendship.addressee_id == user_id,
            Friendship.requester_id == user_id
        ),
        Friendship.status == FriendStatus.accepted
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_friendship(db: AsyncSession, friendship_id: int):
    stmt = select(Friendship).filter(Friendship.id == friendship_id)
    result = await db.execute(stmt)

    friendship = result.scalars().first()

    if not friendship:
        raise FriendshipNotFound()
    return friendship


async def friendship_exists(db: AsyncSession, data: FriendshipCreate) -> bool:
    stmt = select(
        exists().where(
            and_(
                Friendship.addressee_id == data.addressee_id,
                Friendship.requester_id == data.requester_id,
                Friendship.status in [FriendStatus.pending, FriendStatus.accepted]
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalar()


async def send_friendship(db: AsyncSession, data: FriendshipCreate):
    requester = await get_user(db, data.requester_id)
    if requester is None:
        raise UserNotFound()

    if await friendship_exists(db, data):
        raise FriendshipAlreadyExists()

    friendship = Friendship(
        requester_id = data.requester_id,
        addressees_id = data.addressee_id,
        status = data.status
    )

    db.add(friendship)
    await db.commit()
    await db.refresh(friendship)
    return friendship


async def accept_friendship_request(db: AsyncSession, friendship_id: int, data: FriendshipUpdate):
    friendship = await get_friendship(db, friendship_id)

    if data.status is not None:
        friendship.status = FriendStatus.accepted

    await db.commit()
    await db.refresh(friendship)
    return friendship


async def reject_friendship_request(db: AsyncSession, friendship_id: int, data: FriendshipUpdate):
    friendship = await get_friendship(db, friendship_id)

    if data.status is not None:
        friendship.status = FriendStatus.rejected

    await db.commit()
    await db.refresh(friendship)
    return friendship


async def get_friendship_requests(db: AsyncSession, user_id: int):
    stmt = (select(Friendship)
            .filter(Friendship.addressee_id == user_id)
            .where(Friendship.status == FriendStatus.pending))
    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_friendship(db: AsyncSession, friend_id: int, user_id: int):
    stmt = select(Friendship).filter(or_(
            and_(Friendship.addressee_id == friend_id, Friendship.requester_id == user_id),
            and_(Friendship.addressee_id == user_id, Friendship.requester_id == friend_id)
        ),
        Friendship.status == FriendStatus.accepted
    )

    result = await db.execute(stmt)
    friendship = result.scalars().first()

    if not friendship:
        raise FriendshipNotFound()
    await db.delete(friendship)
    await db.commit()

    return True