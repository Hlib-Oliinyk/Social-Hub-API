from sqlalchemy import select, or_, exists, and_
from app.exceptions import FriendshipAlreadyExists
from app.models.friendship import Friendship
from app.schemas.friendship import FriendshipCreate, FriendStatus, FriendshipUpdate, FriendResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_user
from app.exceptions.user import UserNotFound
from app.exceptions.friendship import FriendshipNotFound


async def get_friends(db: AsyncSession, user_id: int):
    stmt = select(Friendship).filter(
        or_(
            Friendship.addressee_id == user_id,
            Friendship.requester_id == user_id
        ),
        Friendship.status == FriendStatus.accepted
    )
    result = await db.execute(stmt)
    friendships = result.scalars().all()

    return [
        FriendResponse(
            friend_id=(
                f.addressee_id if f.requester_id == user_id else f.requester_id
            )
        )
        for f in friendships
    ]


async def get_friendship(db: AsyncSession, friendship_id: int):
    stmt = select(Friendship).filter(Friendship.id == friendship_id)
    result = await db.execute(stmt)

    friendship = result.scalars().first()

    if not friendship:
        raise FriendshipNotFound()
    return friendship


async def friendship_exists(db: AsyncSession, requester_id: int, addressee_id: int) -> bool:
    stmt = select(
        exists().where(
            or_(
                and_(
                    Friendship.addressee_id == addressee_id,
                    Friendship.requester_id == requester_id,
                    Friendship.status.in_([FriendStatus.pending, FriendStatus.accepted])
                ),
                and_(
                    Friendship.addressee_id == requester_id,
                    Friendship.requester_id == addressee_id,
                    Friendship.status.in_([FriendStatus.pending, FriendStatus.accepted])
                )
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalar()


async def send_friendship(db: AsyncSession, data: FriendshipCreate, user_id: int):
    addressee = await get_user(db, data.addressee_id)
    if addressee is None:
        raise UserNotFound()

    if await friendship_exists(db, user_id, data.addressee_id):
        raise FriendshipAlreadyExists()

    friendship = Friendship(
        requester_id = user_id,
        addressee_id = data.addressee_id,
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
    stmt = select(Friendship).where(and_(Friendship.addressee_id == user_id, Friendship.status == FriendStatus.pending))
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