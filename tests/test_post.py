import pytest
from tests.conftest import client, authorized_client, TEST_POST, TEST_COMMENT, TEST_LIKE


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


@pytest.mark.asyncio
async def test_get_post_success(client):
    response = await client.get("/posts/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_comment_success(authorized_client):
    response = await authorized_client.post("/posts/1/comments", json=TEST_COMMENT)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_comment_not_authorized(client):
    response = await client.post("/posts/1/comments", json=TEST_COMMENT)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_add_comment_not_exists(authorized_client):
    response = await authorized_client.post("/posts/2/comments", json={
        "post_id": 2,
        "user_id": 1,
        "content": "nice post"
    })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_like_post_success(authorized_client):
    response = await authorized_client.post("/posts/1/like", json=TEST_LIKE)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_like_post_not_authorized(client):
    response = await client.post("/posts/1/like", json=TEST_LIKE)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unlike_post_success(authorized_client):
    response = await authorized_client.delete("/posts/1/like")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unlike_post_not_exists(authorized_client):
    response = await authorized_client.delete("/posts/2/like")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unlike_post_not_authorized(client):
    response = await client.delete("/posts/1/like")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_not_authorized(client):
    response = await client.delete("/posts/1")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_success(authorized_client):
    response = await authorized_client.delete("/posts/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_post_not_exists(authorized_client):
    response = await authorized_client.delete("/posts/2")
    assert response.status_code == 404