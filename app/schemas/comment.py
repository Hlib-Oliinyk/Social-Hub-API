from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentCreate(BaseModel):
    content: str = Field(min_length=2, max_length=100)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)