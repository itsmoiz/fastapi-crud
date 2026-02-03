from pydantic import BaseModel
from typing import List

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int

class CommentOut(CommentBase):
    id: int

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    file_path: str | None = None
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    posts: List[PostOut] = []

    class Config:
        from_attributes = True
