from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint

from sqlalchemy.engine import base
from starlette.responses import Response

from app.database import Base
from app.models import User

class Post(BaseModel):
    title: str
    content:str
    published: bool = True

class PostCreateResponse(BaseModel):
    pass

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Comments(BaseModel):
    title:str
    content:str  
    post_id:int
 

class CommentsResponseBase(BaseModel):
    id: int
    title:str
    post_id: int
    owner_id:int
    content:str
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True


class CommentsOut(BaseModel):
    Comment:CommentsResponseBase


    

class ResponseBase(BaseModel):
    id: int
    owner_id:int
    title:str
    content:str
    published:bool
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:ResponseBase
    votes:int


class UserCreate(BaseModel):
    email: EmailStr
    password:str



class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
