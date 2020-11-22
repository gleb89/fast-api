from .models import Booking, TimeBooking
from fastapi import HTTPException
from fastapi.responses import JSONResponse


async def create_booking(booking,user,db):
    new_booking = Booking(date = booking.date,user_id=user.id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking



async def new_time_booking(booking_time,db):
    new_booking_time = TimeBooking(time = booking_time.time,booking_id = booking_time.booking_id,is_booking = booking_time.is_booking)
    db.add(new_booking_time )
    db.commit()
    db.refresh(new_booking_time )
    return new_booking_time



async def return_date_user(user_id,db):
    date_all= db.query(Booking).filter(Booking.user_id == user_id).all()
    if date_all:
            return date_all
    else:
        raise HTTPException(status_code=400, detail="Not date")



async def return_time_date(date_id,db):
    time_all = db.query(TimeBooking).filter(TimeBooking.booking_id  == date_id, TimeBooking.is_booking == True ).all()
    if time_all:
            return time_all
    else:
        raise HTTPException(status_code=400, detail="Not time")



async def delete_time_date(time_id,db):
    time = db.query(TimeBooking).filter(TimeBooking.id  == time_id).first()
    db.delete(time)
    db.commit()
    return JSONResponse(status_code=200, content={'message':"Time delete"})



async def update_time_date(time_id,db):
    time = db.query(TimeBooking).filter(TimeBooking.id  == time_id.id).update\
                                                        (dict(is_booking=time_id.is_booking))

    db.commit()
    return JSONResponse(status_code=200, content={'message':"Time update bool"})