from pydantic import BaseModel, ConfigDict
from app.models.friendship import FriendStatus

class FriendshipCreate(BaseModel):
    addressee_id: int
    requester_id: int
    status: FriendStatus


class FriendshipResponse(BaseModel):
    id: int
    addressee_id: int
    status: FriendStatus

    model_config = ConfigDict(from_attributes=True)


class FriendshipUpdate(BaseModel):
    status: FriendStatus | None = None


class FriendResponse(BaseModel):
    friend_id: int