from fastapi import APIRouter, Response, BackgroundTasks, Request
from fastapi.params import Depends

from app.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token
)
from app.dependencies import get_user_service, get_token_service
from app.core.security import create_access_token, create_refresh_token, hash_token
from app.exceptions_handler import InvalidCredentials
from app.services import UserService, TokenService

import app.services.email_service as email_service


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(
    background_tasks: BackgroundTasks,
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    user = await service.create_user(user)
    background_tasks.add_task(email_service.print_welcome_message, user)
    return user


@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    response: Response,
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service)
):
    user = await user_service.authenticate_user(data.email, data.password)
    if user is None:
        raise InvalidCredentials()

    access_token = create_access_token(
        data = {"sub": str(user.id)}
    )

    refresh_token = create_refresh_token()
    refresh_token_hash = hash_token(refresh_token)
    await token_service.save_new_token(user.id, refresh_token_hash)

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
async def logout(
    request: Request,
    response: Response,
    service: TokenService = Depends(get_token_service)
):
    refresh_token = request.cookies.get("refresh_token")
    await service.delete_refresh_token(refresh_token)

    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")

    return {
        "detail": "Logged out"
    }


@router.post("/refresh")
async def refresh(
    response: Response,
    request: Request,
    service: TokenService = Depends(get_token_service)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidCredentials()

    new_refresh, new_access = await service.rotate_refresh_token(refresh_token)

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