import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.db.database import Base, test_async_engine, AsyncSessionTest
from app.dependencies import get_db
from app.main import app
from tests.data import TEST_USER, TEST_USER_LOGIN, TEST_POST, TEST_ANOTHER_USER,TEST_ANOTHER_USER_LOGIN


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


def make_client_fixture():
    @pytest_asyncio.fixture
    async def _client():
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            yield ac
    return _client


client = make_client_fixture()
clean_client = make_client_fixture()


def make_user_fixtures(user_data, user_login):
    @pytest_asyncio.fixture
    async def registered_user(client):
        await client.post("/auth/register", json=user_data)


    @pytest_asyncio.fixture
    async def authorized_client(client, registered_user):
        response = await client.post("/auth/login", json=user_login)
        assert response.status_code == 200
        return client

    return registered_user, authorized_client


registered_user, authorized_client = make_user_fixtures(TEST_USER, TEST_USER_LOGIN)
registered_second_user, authorized_second_client = make_user_fixtures(
    TEST_ANOTHER_USER, TEST_ANOTHER_USER_LOGIN
)


@pytest_asyncio.fixture
async def registered_post(authorized_client):
    response = await authorized_client.post("/posts", json=TEST_POST)
    assert response.status_code == 200
    return response.json()["id"]


@pytest_asyncio.fixture
async def registered_like(authorized_client, registered_post):
    response = await authorized_client.post(f"/posts/{registered_post}/like")
    assert response.status_code == 200
    return response.json()


@pytest_asyncio.fixture
async def registered_another_user(client):
    response = await client.post("/auth/register", json=TEST_ANOTHER_USER)
    assert response.status_code == 200
    return response.json()


@pytest_asyncio.fixture
async def authorized_another_client(client, registered_another_user):
    response = await client.post("/auth/login", json=TEST_ANOTHER_USER_LOGIN)
    assert response.status_code == 200
    return client