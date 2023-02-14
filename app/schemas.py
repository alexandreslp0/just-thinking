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
    id: int
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


class PostUpdateBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreateResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner: UserPostResponse

    class Config:
        orm_mode = True

        
class PostFullResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner: UserPostResponse
    comments: int

    class Config:
        orm_mode = True


class Test(PostCreateResponse):
    posts: PostCreateResponse
    comments: int

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str


class CommentFullResponse(BaseModel):
    id: int
    owner_id: int
    post_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
