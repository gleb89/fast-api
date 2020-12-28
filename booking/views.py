from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from .schemas import BookingBase, BookingCreate, BookingTimeCreate,TimeConf,\
                                         TimeUpdateBool, BookingTimeCheck,\
                                                        BookingTimeCostum
from .crud import create_booking, new_time_booking, return_date_user,\
    return_time_date, delete_time_date,master_confirm_time,\
    return_time_date_all, check_time_owner,\
    create_booking_costum
from .models import Booking, TimeBooking
from users_profile.crud import get_current_active_user
from users_profile.schemas import User


booking_router = APIRouter()


@booking_router.post('/booking-create_date')
async def create_date(booking:BookingCreate, db: Session = Depends(get_db)):
    """Create new date user booking"""
    new_booking = await create_booking(booking,db)
    return new_booking


@booking_router.post('/booking-create_time')
async def create_time_master(booking_time:BookingTimeCreate,
                        db:Session = Depends(get_db)):
    """Create new time user booking_date"""
    new_time = await new_time_booking(booking_time, db)
    return new_time


@booking_router.get('/booking-data/{user_id}')
async def data_all_master(user_id:int, db:Session = Depends(get_db)):
    """Return  date in user booking_date"""
    date = await return_date_user(user_id, db)
    print('nn')
    return date


@booking_router.get('/booking_time/{date_id}')
async def time_all_master(date_id:int, db: Session = Depends(get_db)):
    """Return  date in user booking_date"""
    time = await return_time_date(date_id, db)
    return time


@booking_router.get('/booking_time')
async def time_user_all(date:str, user:int, db:Session = Depends(get_db)):
    """Return  time in user booking_date"""
    time = await return_time_date_all(date, user, db)
    return time


@booking_router.delete('/booking_time/{time_id}')
async def time_delete_master(time_id:int, db:Session = Depends(get_db)):
    """Delete  time in user booking_date"""
    response = await delete_time_date(time_id, db)
    return response


@booking_router.put('/check-time/')
async def time_chech(time:BookingTimeCheck, db:Session = Depends(get_db)):
    """Zapis check time user auth in master"""
    check_time = await check_time_owner(time, db)
    return check_time


@booking_router.post('/zapis-time/')
async def time_data_create(time_data:BookingTimeCostum, db:Session = Depends(get_db)):
    """create costum time user auth"""
    time = await create_booking_costum(time_data, db)
    return time

@booking_router.put('/confirm-time/')
async def confirm_master_time(time_data:TimeConf, db:Session = Depends(get_db)):
    """coinfirm master time"""
    time = await master_confirm_time(time_data, db)
    return time
