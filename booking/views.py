from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import  get_db
from .schemas import BookingBase, BookingCreate, BookingTimeCreate, TimeUpdateBool
from .crud import create_booking, new_time_booking, return_date_user,\
                                     return_time_date, delete_time_date,update_time_date
from .models import Booking, TimeBooking
from users_profile.crud import get_current_active_user
from users_profile.schemas import User



booking_router = APIRouter()



@booking_router.post('/booking-create_date')
async def create_date(booking: BookingCreate,user: User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    """Create new date user booking"""
    new_booking = await create_booking(booking,user,db)
    return new_booking



@booking_router.post('/booking-create_time')
async def create_time(booking_time: BookingTimeCreate, user: User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    """Create new time user booking_date"""
    new_time = await new_time_booking(booking_time,db)
    return new_time



@booking_router.get('/booking-data/{user_id}')
async def data_all(user_id:int,db: Session = Depends(get_db)):
    """Return  date in user booking_date"""
    date = await return_date_user(user_id,db)
    return date




@booking_router.get('/booking_time/{date_id}')
async def time_all(date_id:int,db: Session = Depends(get_db)):
    """Return  date in user booking_date"""
    time = await return_time_date(date_id,db)
    return time



@booking_router.delete('/booking_time/{time_id}')
async def time_delete(time_id:int ,db: Session = Depends(get_db)):
    """Delete  time in user booking_date"""
    response = await delete_time_date(time_id,db)
    return response



@booking_router.put('/booking_time_bool/')
async def time_delete(time_boll:TimeUpdateBool,user: User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    """Update time bool if booking"""
    response = await update_time_date(time_boll,db)
    return response