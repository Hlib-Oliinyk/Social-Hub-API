import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.db.database import Base, test_async_engine, AsyncSessionTest
from app.dependencies import get_db
from app.main import app

TEST_USER = {
    "email": "test@gmail.com",
    "username": "test",
    "password": "secretpassword"
}

TEST_USER_LOGIN = {
    "email": "test@gmail.com",
    "password": "secretpassword"
}

TEST_POST = {
    "user_id": 1,
    "content": "Yooo jordan"
}

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


@pytest_asyncio.fixture
async def registered_user(client):
    await client.post("/auth/register", json=TEST_USER)


@pytest_asyncio.fixture
async def authorized_client(client, registered_user):
    response = await client.post("/auth/login", json=TEST_USER_LOGIN)
    assert response.status_code == 200
    return client