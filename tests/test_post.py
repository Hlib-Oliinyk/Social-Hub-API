import pytest
from tests.conftest import client, authorized_client, TEST_POST


@pytest.mark.asyncio
async def test_get_posts(client):
    response = await client.get("/posts")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_post_not_exists(client):
    response = await client.get("/posts/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_post(authorized_client):
    response = await authorized_client.post("/posts", json=TEST_POST)
    assert response.status_code == 200