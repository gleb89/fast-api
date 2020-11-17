from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from users_profile.schemas import UserInRoom, UserInChat


class RoomBase(BaseModel):
    date: Optional[datetime]
    owner_id:int
    date: Optional[datetime]



class RoomCreate(BaseModel):
    owner_id:int
    date: Optional[datetime]

    class Config:
        orm_mode = True



class ChatBase(BaseModel):
    text: str
    date: Optional[datetime]
    user_id:int


class ChatCreate(ChatBase):
    pass
    class Config:
        orm_mode = True
