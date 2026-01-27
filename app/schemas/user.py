from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str = Field(min_length=3, max_length=25)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    password: str = Field(min_length=8)
