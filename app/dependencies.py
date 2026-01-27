from fastapi import HTTPException
from fastapi.params import Depends
from app.db.database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.schemas.token import TokenData
from app.services.user_service import get_user
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(db: AsyncSession = Depends(get_db)
                           ,token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = await get_user(db, user_id=token_data.user_id)

    if user is None:
        raise credentials_exception

    return user