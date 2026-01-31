from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LikeCreate(BaseModel):
    user_id: int
    post_id: int


class LikeResponse(BaseModel):
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)