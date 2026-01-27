from fastapi import HTTPException
from fastapi import Request
from fastapi.params import Depends
from app.db.database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.services.user_service import get_user
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


async def get_token_from_header_or_cookie(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]

    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token

    raise credentials_exception


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token_from_header_or_cookie)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    user = await get_user(db, user_id=user_id)

    if user is None:
        raise credentials_exception

    return user