from fastapi import APIRouter, Response, BackgroundTasks, Request
from fastapi.params import Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.core.security import create_access_token, create_refresh_token
import app.services.user_service as user_service
import app.services.email_service as email_service
import app.services.token_service as token_service
from app.exceptions_handler import InvalidCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(background_tasks: BackgroundTasks, user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_service.create_user(db, user)
    background_tasks.add_task(email_service.print_welcome_message, user)
    return user


@router.post("/login", response_model=Token)
async def login(data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    user = await user_service.authenticate_user(db, data.email, data.password)

    if user is None:
        raise InvalidCredentials()

    access_token = create_access_token(
        data = {"sub": str(user.id)}
    )

    refresh_token = create_refresh_token()
    refresh_token_hash = token_service.hash_token(refresh_token)
    await token_service.save_new_token(db, user.id, refresh_token_hash)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 14
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    await token_service.delete_refresh_token(db, refresh_token)

    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")

    return {
        "detail": "Logged out"
    }


@router.post("/refresh")
async def refresh(response: Response, request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise InvalidCredentials()

    new_refresh, new_access = await token_service.rotate_refresh_token(db, refresh_token)

    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 14
    )

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }