from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class PostCreate(BaseModel):
    content: str = Field(min_length=2, max_length=1000)


class PostRead(BaseModel):
    id: int
    username: str
    content: str
    likes_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostPagination(BaseModel):
    limit: int = Field(5, ge=0, le=100)
    offset: int = Field(0, ge=0)