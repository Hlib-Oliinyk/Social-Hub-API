from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.core.security import create_access_token
import app.services.user_service as user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, user)


@router.post("/login", response_model=Token)
async def login(data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    user = await user_service.authenticate_user(db, data.email, data.password)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data = {"sub": str(user.id)}
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {
        "detail": "Logged out"
    }
