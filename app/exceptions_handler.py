from fastapi.responses import JSONResponse
from app.exceptions import *


def setup_exception_handler(app):
    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail":"User not found"}
        )

    @app.exception_handler(UserAlreadyExists)
    async def user_exists_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail":"User exists"}
        )

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(request, exc):
        return JSONResponse(
            status_code=401,
            content={"detail":"Could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"}
        )

