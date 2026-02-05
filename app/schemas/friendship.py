from pydantic import BaseModel, ConfigDict
from app.models import FriendStatus

class FriendshipCreate(BaseModel):
    addressee_id: int
    status: FriendStatus


class FriendshipResponse(BaseModel):
    id: int
    addressee_id: int
    status: FriendStatus

    model_config = ConfigDict(from_attributes=True)


class FriendResponse(BaseModel):
    id: int
    friend_name: str

    model_config = ConfigDict(from_attributes=True)