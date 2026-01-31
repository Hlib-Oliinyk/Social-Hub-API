import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.db.database import Base, test_async_engine, AsyncSessionTest
from app.dependencies import get_db
from app.main import app

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async with AsyncSessionTest() as db:
        yield db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac