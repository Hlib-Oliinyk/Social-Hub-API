import pytest
from tests.conftest import client, registered_user, authorized_client


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "email": "test@gmail.com",
        "username": "test",
        "password": "secretpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "test"


@pytest.mark.asyncio
async def test_register_user_exists(client):
    response = await client.post("/auth/register", json={
        "email": "test@gmail.com",
        "username": "test",
        "password": "secretpassword"
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client, registered_user):
    response = await client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "secretpassword"
    })
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