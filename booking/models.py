from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, sql, Date,Time
from config.db import Base
from sqlalchemy.orm import relationship


class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User",foreign_keys=[user_id])


booking= Booking.__table__



class TimeBooking(Base):
    __tablename__ = "booking_time"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time)
    is_booking = Column(Boolean, default=True)
    booking_id = Column(Integer, ForeignKey("booking.id"))

    booking = relationship("Booking",foreign_keys=[booking_id])


booking_time= TimeBooking.__table__