from typing import List, Optional
from pydantic import BaseModel
from typing import List
from pydantic import EmailStr
import uuid
import pydantic


class Category(BaseModel):
    title:str


class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    master:bool


class UserUpdate(User):
    category:int
    name: str
    email: Optional[str] = None
    city:str


class UserInDB(User):
    name: str
    category:int

class UserInDfB(User):
    hashed_password: str

class UserIMage(User):
    avatar: str = None



class UserCreate(BaseModel):
    name: str
    password: str
    email: Optional[str] = None
    city:str
    master:bool
    category_id:int
    phone:str

class UsId(User):
    id:int
    rating:int


class UserLogin(BaseModel):
    email: Optional[str] = None
    password: str



class UserAuthenticate(User):
    password: str


class UserInfo(User):
    city:str
    master:bool
    avatar:str
    rating:int

    class Config:
        orm_mode = True


#user  chat room
class UserInRoom(BaseModel):
    id: Optional[str]

    @pydantic.validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or str(uuid.uuid4())

class UserInChat(BaseModel):
    id: Optional[str]


    @pydantic.validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or str(uuid.uuid4())

    class Config:
        orm_mode = True



#JWT Tocken
class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    email: Optional[str] = None



#email
class EmailSchema(BaseModel):
    email: str



class EmailRessetPassword(EmailSchema):
    password:str
    new_password:str
    email:str