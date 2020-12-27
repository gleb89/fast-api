from typing import List, Optional
from pydantic import BaseModel
from datetime import date, time


class BookingBase(BaseModel):
    id: int
    user_id: int
    date: Optional[date]


class BookingCreate(BaseModel):
    date: Optional[date]
    user_id:int


class TimeUpdateBool(BaseModel):
    id: int
    is_booking: bool


class TimeConf(BaseModel):
    id: int
    master_confirm: bool


class BookingTimeBase(BaseModel):
    id: int
    booking_id: int
    time: Optional[time]


class BookingTimeCreate(BaseModel):
    user_id:int
    time: Optional[time]
    date:Optional[date]
    is_booking: bool


class BookingTimeCheck(BaseModel):
    id: int
    is_booking: bool
    owner_id: int
    phone_owner:str


class BookingTimeCostum(BaseModel):
    user_id: int
    owner_id: int
    phone_owner:str
    date: Optional[date]
    time: Optional[time]
