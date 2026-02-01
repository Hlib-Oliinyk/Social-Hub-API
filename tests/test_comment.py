import pytest
from tests.data import TEST_COMMENT

@pytest.mark.asyncio
async def test_add_comment_success(authorized_client, registered_post):
    response = await authorized_client.post(f"/posts/{registered_post}/comments", json=TEST_COMMENT)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_comment_unauthorized(clean_client, registered_post):
    response = await clean_client.post(f"/posts/{registered_post}/comments", json=TEST_COMMENT)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_add_comment_not_exists(authorized_client):
    response = await authorized_client.post("/posts/888/comments", json={
        "post_id": 888,
        "user_id": 1,
        "content": "nice post"
    })
    assert response.status_code == 404