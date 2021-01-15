from .models import Booking, TimeBooking
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from users_profile.models import User


async def create_booking(booking, db):
    user = booking.user_id
    new_booking = Booking(date=booking.date, user_id=user)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


async def new_time_booking_costum(data, booking_id, db):
    new_booking_time = TimeBooking(
        time=data.time, owner_id=data.owner_id, booking_id=booking_id, is_booking=True, phone_owner = data.phone_owner)
    db.add(new_booking_time)
    db.commit()
    db.refresh(new_booking_time)
    return new_booking_time


async def create_booking_costum(time_data, db):
    date = db.query(Booking).filter(Booking.user_id ==
                                    time_data.user_id, Booking.date == time_data.date).first()
    if date:
        time = await new_time_booking_costum(time_data, date.id, db)
        time_add = date.time.append(time)
        db.commit()
        db.refresh(time)
        return time
    else:
        data = await create_booking(time_data, db)
        time = await new_time_booking_costum(time_data, data.id, db)

        time_add = data.time.append(time)
        db.commit()
        db.refresh(time)
        return time




async def time(booking_time,data_id,db):
    new_booking_time = TimeBooking(
    time=booking_time.time, booking_id=data_id, is_booking=booking_time.is_booking, phone_owner = '')
    db.add(new_booking_time)
    db.commit()
    db.refresh(new_booking_time)
    return new_booking_time



async def new_time_booking(booking_time, db):
    date = db.query(Booking).filter(Booking.user_id ==
                                    booking_time.user_id, Booking.date == booking_time.date).first()
    if date:
        time_new = await time(booking_time, date.id, db)
        time_add = date.time.append(time_new)
        # db.add(time_add)
        db.commit()
        # db.refresh(time_add)
        db.refresh(time_new)
        return time_new
    else:
        data = await create_booking(booking_time,db)
        time_new = await time(booking_time, data.id, db)
        time_add = data.time.append(time_new)
        # db.add(time_add)
        db.commit()
        # db.refresh(time_add)
        db.refresh(time_new)
        return time_new


# user.children.append(new_rating)


async def return_date_user(user_id, db):
    date_all = db.query(Booking).filter(Booking.user_id == user_id).all()
    if date_all:
        for i in date_all:
            print(i.time)
        return date_all
    else:
        raise HTTPException(status_code=400, detail="Not date")


async def user_date_time(date_id,db):
        date = db.query(Booking).filter(Booking.id ==
                                    date_id).first()
        user = db.query(User).filter(
            User.id == date.user_id).first()
        return {'user_name':user.name,'date':date.date,'user_category':user.category}


async def return_time_owner(owner_id, db):
    list_time = []
    time_all = db.query(TimeBooking).filter(
            TimeBooking.owner_id == owner_id).all()
    if time_all:
        for i in time_all:
            date_user = await user_date_time(i.booking_id,db)
            list_dict_time = {
                "name_master": date_user['user_name'],
                "phone_master": "12",
                "time": i.time,
                "date":  date_user['date'],
                "master_confirm": i.master_confirm,
                'user_category':date_user['user_category']
            }
            list_time.append(list_dict_time)
        return list_time

    else:
        return None



async def return_time_date_all(date, user_id, db):
    date_all = db.query(Booking).filter(Booking.user_id ==
                                        user_id, Booking.date == date).first()

    if date_all:
        time_all = db.query(TimeBooking).filter(
            TimeBooking.booking_id == date_all.id, TimeBooking.owner_id == None).all()
        if time_all:
            return time_all
        else:
            return None
    else:
        return None


async def owner_name(owner_id, db):
    user = db.query(User).filter(
        User.id == owner_id).first()
    print(user.name)
    return {'user_name':user.name}

async def return_time_date(date_id, db):
    list_time = []
    time_all = db.query(TimeBooking).filter(
        TimeBooking.booking_id == date_id).all()
    
    if time_all:
        for i in time_all:
            owner_id = await owner_name(i.owner_id, db)
            data_time = {
            "owner_id": owner_id['user_name'],
            "booking_id": i.booking_id,
            "master_confirm": i.master_confirm,
            "time": i.time,
            "phone_owner": i.phone_owner,
            "is_booking": i.is_booking,
            "id": i.id
            }
            
            list_time.append(data_time)
        return list_time
    else:
        raise HTTPException(status_code=400, detail="Not time")
    return list_time

#rett
async def delete_time_date(time_id, db):
    time = db.query(TimeBooking).filter(TimeBooking.id == time_id).first()
    db.delete(time)
    db.commit()
    return JSONResponse(status_code=200, content={'message': "Time delete"})


async def check_time_owner(time, db):
    db.query(TimeBooking).filter(TimeBooking.id == time.id).update(
        dict(is_booking=True, owner_id=time.owner_id,phone_owner = time.phone_owner))
    db.commit()
    return JSONResponse(status_code=200, content={'message': "Time update user bool"})



async def master_confirm_time(time_data,db):
    time = db.query(TimeBooking).filter(TimeBooking.id == time_data.id).update\
                                (dict(master_confirm = time_data.master_confirm,\
                                                            is_booking = False))
    db.commit()
    return time
