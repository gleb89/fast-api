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



class UserInDB(User):
    name: str

class UserIMage(User):
    avatar: str = None



class UserCreate(BaseModel):
    name: str
    password: str

class UsId(User):
    id:int

class UserLogin(BaseModel):
    name: str
    password: str

class UserAuthenticate(User):
    password: str


class UserInfo(User):
    id: int

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
    name: Optional[str] = None



#email
class EmailSchema(BaseModel):
    email: str



class EmailRessetPassword(EmailSchema):
    password:str