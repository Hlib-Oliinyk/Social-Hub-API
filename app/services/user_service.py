from fastapi import HTTPException
from app.core.security import hash_password, verify_password
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, exists
from app.schemas.user import UserCreate


async def get_users(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def user_exists(db: AsyncSession, email: str, username: str) -> bool:
    stmt = select(
        exists().where(
            or_(User.username == username, User.email == email)
        )
    )
    result = await db.execute(stmt)
    return result.scalar()


async def create_user(db: AsyncSession, data: UserCreate):
    if await user_exists(db, data.email, data.username):
        raise HTTPException(status_code=400, detail="User exists")

    user = User(
        email = data.email,
        username = data.username,
        hashed_password = hash_password(data.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)

    await db.delete(user)
    await db.commit()
    return True


async def authenticate_user(db: AsyncSession, login: str, password: str) -> User | None:
    stmt = select(User).filter(or_(User.username == login, User.email == login))
    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user