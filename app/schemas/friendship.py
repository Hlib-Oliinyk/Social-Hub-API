from pydantic import BaseModel
from app.models.friendship import FriendStatus

class FriendshipCreate(BaseModel):
    addressee_id: int
    requester_id: int
    status: FriendStatus


class FriendshipResponse(BaseModel):
    addressee_name: str
    status: FriendStatus