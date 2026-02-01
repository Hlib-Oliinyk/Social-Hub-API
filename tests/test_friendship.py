import pytest
from tests.data import TEST_FRIENDSHIP

@pytest.mark.asyncio
async def test_get_friends_success(authorized_client):
    response = await authorized_client.get("/friends")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_friends_unauthorized(clean_client):
    response = await clean_client.get("/friends")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_friendship_requests_success(authorized_client):
    response = await authorized_client.get("/friends/requests")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_friendship_requests_unauthorized(clean_client):
    response = await clean_client.get("/friends/requests")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_send_friendship_request_success(authorized_client, registered_another_user):
    response = await authorized_client.post(f"/friends/{registered_another_user["id"]}",
                                            json=TEST_FRIENDSHIP)
    assert response.status_code == 200