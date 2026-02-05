from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models import RefreshToken


class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_validate_refresh_token(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def save_token(self, **data) -> RefreshToken:
        refresh_token = RefreshToken(**data)
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def rotate_tokens_data(self, old_token_id: int, user_id: int, new_hash: str) -> RefreshToken:
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.id == old_token_id)
            .values(is_revoked = True)
        )

        new_token = RefreshToken(
            user_id = user_id,
            token = new_hash,
            expires_at = datetime.now(timezone.utc) + timedelta(days=14)
        )

        self.db.add(new_token)
        await self.db.commit()
        await self.db.refresh(new_token)
        return new_token

    async def delete_token(self, token_hash: str):
        stmt = update(RefreshToken).where(RefreshToken.token == token_hash).values(is_revoked = True)
        await self.db.execute(stmt)
        await self.db.commit()
