from datetime import datetime, timezone, timedelta
from fastapi import Request

from app.models import RefreshToken
from app.exceptions_handler import InvalidCredentials
from app.core.security import (
    hash_token,
    create_refresh_token,
    create_access_token
)
from app.repositories import TokenRepository


class TokenService:
    def __init__(self, repo: TokenRepository):
        self.repo = repo

    async def get_validate_refresh_token(self, token: str) -> RefreshToken:
        refresh_token = await self.repo.get_validate_refresh_token(token)
        if refresh_token is None:
            raise InvalidCredentials()
        return refresh_token

    async def save_new_token(self, user_id: int, token: str) -> RefreshToken:
        return await self.repo.save_token(
            user_id = user_id,
            token = token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=14)
        )

    async def rotate_refresh_token(self, token: str):
        token_hash = hash_token(token)

        old_token = await self.repo.get_validate_refresh_token(token_hash)
        if old_token is None:
            raise InvalidCredentials()

        new_refresh = create_refresh_token()
        new_refresh_hash = hash_token(new_refresh)

        await self.repo.rotate_tokens_data(
            old_token_id = old_token.id,
            user_id = old_token.user_id,
            new_hash = new_refresh_hash
        )

        new_access = create_access_token(data = {"sub": str(old_token.user_id)})
        return new_refresh, new_access

    async def delete_refresh_token(self, token: str):
        token_hash = hash_token(token)
        await self.repo.delete_token(token_hash)

    @staticmethod
    async def get_token_from_header_or_cookie(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]

        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            return cookie_token

        raise InvalidCredentials()