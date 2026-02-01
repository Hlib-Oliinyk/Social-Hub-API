import pytest
from tests.conftest import client

@pytest.mark.asyncio
async def test_me_authorized(authorized_client):
    response = await authorized_client.get("/users/me")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_me_unauthorized(clean_client):
    response = await clean_client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_user_success(client):
    response = await client.get("/users/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_wrong_id(client):
    response = await client.get("/users/2")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_unauthorized(clean_client):
    response = await clean_client.delete("/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_success(authorized_client):
    response = await authorized_client.delete("/users/me")
    assert response.status_code == 200