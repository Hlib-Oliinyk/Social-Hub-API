import pytest
from tests.conftest import client, registered_user, authorized_client
from tests.data import TEST_USER, TEST_USER_LOGIN


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["username"] == "test"


@pytest.mark.asyncio
async def test_register_user_exists(client):
    response = await client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client, registered_user):
    response = await client.post("/auth/login", json=TEST_USER_LOGIN)
    assert response.status_code == 200
    assert "access_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client, registered_user):
    response = await client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(authorized_client):
    response = await authorized_client.post("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in response.cookies