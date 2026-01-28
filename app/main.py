from fastapi import FastAPI
from app.api.v1 import *
from app.exceptions_handler import setup_exception_handler

app = FastAPI(
    docs_url="/api/docs"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(friendships_router)

setup_exception_handler(app)

@app.get("/")
def root():
    return {
        "message": "Social Hub API",
        "docs": "/api/docs"
    }