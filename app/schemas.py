from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserFullResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserPostResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostFullResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserPostResponse

    class Config:
        orm_mode = True
