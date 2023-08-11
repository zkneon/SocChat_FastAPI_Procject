from datetime import datetime
from auth.schemas import UserRead
from pydantic import BaseModel
from typing import Dict, Any


class Posts(BaseModel):
    user_id: int
    title: str
    message: str
    add_message_at: datetime


class PostsGet(Posts):
    id: int
    user_id: int
    add_message_at: datetime
    title: str
    message: str
    user: str
    like_post_id: int
    like: str

    class Config:
        orm_mode = True


class LikePost(BaseModel):
    id: int
    like_q: int
    dislike_q: int
    who: list[int]

    class Config:
        orm_mode = True


class PostsAdd(BaseModel):
    user_id: int
    title: str
    message: str

