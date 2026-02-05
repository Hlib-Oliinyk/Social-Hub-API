from datetime import datetime, timezone, timedelta
from fastapi import Request
from sqlalchemy import select, update

from app.models import RefreshToken
from app.exceptions_handler import InvalidCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import (
    hash_token,
    create_refresh_token,
    create_access_token
)


async def get_token_from_header_or_cookie(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token

    raise InvalidCredentials()


async def get_valid_refresh_token(token: str, db: AsyncSession):
    stmt = select(RefreshToken).where(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    )
    result = await db.execute(stmt)
    refresh_token = result.scalar_one_or_none()

    if refresh_token is None:
        raise InvalidCredentials()
    return refresh_token


async def save_new_token(db: AsyncSession, user_id: int, token: str):
    new_token = RefreshToken(
            user_id = user_id,
            token = token,
            expires_at = datetime.now(timezone.utc) + timedelta(days=14)
        )

    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)

    return new_token


async def rotate_refresh_token(db: AsyncSession, token: str):
    token_hash = hash_token(token)

    old_token = await get_valid_refresh_token(token_hash, db)
    old_token.is_revoked = True

    new_refresh = create_refresh_token()
    new_refresh_hash = hash_token(new_refresh)

    await save_new_token(db, old_token.user_id, new_refresh_hash)
    await db.commit()

    new_access = create_access_token(data = {"sub": str(old_token.user_id)})
    return new_refresh, new_access


async def delete_refresh_token(db: AsyncSession, token: str):
    token_hash = hash_token(token)

    stmt = update(RefreshToken).where(RefreshToken.token == token_hash).values(is_revoked = True)
    await db.execute(stmt)
    await db.commit()