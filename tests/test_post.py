import pytest
from tests.conftest import client, authorized_client
from tests.data import TEST_POST


@pytest.mark.asyncio
async def test_get_posts(client):
    response = await client.get("/posts")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_post_not_exists(client):
    response = await client.get("/posts/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_post(authorized_client):
    response = await authorized_client.post("/posts", json=TEST_POST)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_post_success(client, registered_post):
    response = await client.get(f"/posts/{registered_post}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_post_unauthorized(clean_client, registered_post):
    response = await clean_client.delete(f"/posts/{registered_post}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_success(authorized_client, registered_post):
    response = await authorized_client.delete(f"/posts/{registered_post}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_post_not_exists(authorized_client):
    response = await authorized_client.delete("/posts/999")
    assert response.status_code == 404