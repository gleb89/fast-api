from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime



class RoomBase(BaseModel):
    date: Optional[datetime]
    owner_id:int
    invited_id:int




class RoomCreate(BaseModel):
    owner_id:int
    invited_id:int
    date: Optional[datetime]

    class Config:
        orm_mode = True



class ChatBase(BaseModel):
    text: str
    user_id:int
    room_id:int
    date: Optional[datetime]



class ChatCreate(BaseModel):
    text: str
    user_id:int
    room_id:int
    date: Optional[datetime]

    class Config:
        orm_mode = True
