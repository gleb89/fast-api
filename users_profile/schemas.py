from typing import List, Optional
from pydantic import BaseModel
from typing import List
from pydantic import EmailStr



class User(BaseModel):
    name: str
    email: Optional[str] = None



class UserInDB(User):
    password: str



class UserCreate(User):
    password: str



class UserAuthenticate(User):
    password: str


class UserInfo(User):
    id: int

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