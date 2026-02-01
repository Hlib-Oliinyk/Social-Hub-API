import pytest

@pytest.mark.asyncio
async def test_like_post_success(authorized_client, registered_post):
    response = await authorized_client.post(f"/posts/{registered_post}/like")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_like_post_unauthorized(clean_client, registered_post):
    response = await clean_client.post(f"/posts/{registered_post}/like")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unlike_post_success(authorized_client, registered_post, registered_like):
    response = await authorized_client.delete(f"/posts/{registered_post}/like")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unlike_post_not_exists(authorized_client):
    response = await authorized_client.delete("/posts/999/like")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unlike_post_unauthorized(clean_client, registered_post):
    response = await clean_client.delete(f"/posts/{registered_post}/like")
    assert response.status_code == 401