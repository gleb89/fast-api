from .models import Booking, TimeBooking
from fastapi import HTTPException
from fastapi.responses import JSONResponse


async def create_booking(booking, user, db):
    try:
        user = user.id
    except :
        user = user
    new_booking = Booking(date=booking.date, user_id=user)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


async def new_time_booking_costum(data, booking_id, db):
    new_booking_time = TimeBooking(
        time=data.time, owner_id=data.owner_id, booking_id=booking_id, is_booking=False, phone_owner = data.phone_owner)
    db.add(new_booking_time)
    db.commit()
    db.refresh(new_booking_time)
    return new_booking_time


async def create_booking_costum(time_data, db):
    date = db.query(Booking).filter(Booking.user_id ==
                                    time_data.user_id, Booking.date == time_data.date).first()
    if date:
        time = await new_time_booking_costum(time_data, date.id, db)
        return time
    else:
        date = await create_booking(time_data, time_data.user_id, db)
        time = await new_time_booking_costum(time_data, date.id, db)
        try:
            return JSONResponse(status_code=200, content={'message': "Time create"})
        except:
            raise HTTPException(status_code=400, detail="Not time")


async def new_time_booking(booking_time, db):
    new_booking_time = TimeBooking(
        time=booking_time.time, booking_id=booking_time.booking_id, is_booking=booking_time.is_booking, phone_owner = '')
    db.add(new_booking_time)
    db.commit()
    db.refresh(new_booking_time)
    return new_booking_time


async def return_date_user(user_id, db):
    date_all = db.query(Booking).filter(Booking.user_id == user_id).all()
    if date_all:
        return date_all
    else:
        raise HTTPException(status_code=400, detail="Not date")


async def return_time_date_all(date, user_id, db):
    date_all = db.query(Booking).filter(Booking.user_id ==
                                        user_id, Booking.date == date).first()

    if date_all:
        time_all = db.query(TimeBooking).filter(
            TimeBooking.booking_id == date_all.id, TimeBooking.is_booking == True).all()
        if time_all:
            return time_all
        else:
            return None
    else:
        return None


async def return_time_date(date_id, db):
    time_all = db.query(TimeBooking).filter(
        TimeBooking.booking_id == date_id, TimeBooking.is_booking == True).all()
    if time_all:
        return time_all
    else:
        raise HTTPException(status_code=400, detail="Not time")


async def delete_time_date(time_id, db):
    time = db.query(TimeBooking).filter(TimeBooking.id == time_id).first()
    db.delete(time)
    db.commit()
    return JSONResponse(status_code=200, content={'message': "Time delete"})


async def check_time_owner(time, db):
    db.query(TimeBooking).filter(TimeBooking.id == time.id).update(
        dict(is_booking=False, owner_id=time.owner_id,phone_owner = time.phone_owner))
    db.commit()
    return JSONResponse(status_code=200, content={'message': "Time update user bool"})
