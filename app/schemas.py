from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    #rating: Optional[int] = None

class CreateUsers(BaseModel):
    email: EmailStr
    password:str

class UsersCreateResp(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    passwd: str

class Token(BaseModel):
    token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)