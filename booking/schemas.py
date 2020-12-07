from typing import List, Optional
from pydantic import BaseModel
from datetime import date,time



class BookingBase(BaseModel):
    id:int
    user_id:int
    date: Optional[date]



class BookingCreate(BaseModel):
    date: Optional[date]

class TimeUpdateBool(BaseModel):
    id:int
    is_booking:bool




class BookingTimeBase(BaseModel):
    id:int
    booking_id:int
    time: Optional[time]

class BookingTimeCreate(BaseModel):
    booking_id:int
    time: Optional[time]
    is_booking:bool


class BookingTimeCheck(BaseModel):
    id:int
    is_booking:bool
    owner_id:int
