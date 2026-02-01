import pytest
from tests.data import TEST_USER, TEST_USER_LOGIN


@pytest.mark.asyncio
async def test_register_user(clean_client):
    response = await clean_client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["username"] == "test"


@pytest.mark.asyncio
async def test_register_user_exists(clean_client):
    response = await clean_client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(clean_client, registered_user):
    response = await clean_client.post("/auth/login", json=TEST_USER_LOGIN)
    assert response.status_code == 200
    assert "access_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(clean_client, registered_user):
    response = await clean_client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(authorized_client):
    response = await authorized_client.post("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in response.cookies