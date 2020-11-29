from typing import List, Optional
from pydantic import BaseModel
from typing import List
from pydantic import EmailStr
import uuid
import pydantic



class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    master:bool




class UserInDB(User):
    name: str

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

class UsId(User):
    id:int

class UserLogin(BaseModel):
    email: Optional[str] = None
    password: str

class UserAuthenticate(User):
    password: str


class UserInfo(User):
    city:str
    master:bool
    avatar:str

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