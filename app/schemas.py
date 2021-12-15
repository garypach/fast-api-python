from pydantic import BaseModel,EmailStr
from datetime import datetime


class ResponseBase(BaseModel):
    id: int
    title:str
    content:str
    published:bool
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password:str

class UserOut(BaseModel):
    id:str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True