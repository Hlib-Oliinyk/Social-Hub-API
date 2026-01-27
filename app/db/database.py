from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import DATABASE_URL

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass