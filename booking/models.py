from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, sql, Date,Time,Table
from config.db import Base
from sqlalchemy.orm import relationship


date_table = Table('date_time', Base.metadata,
    Column('booking', Integer, ForeignKey('booking.id')),
    Column('booking_time', Integer, ForeignKey('booking_time.id')
    ),
    extend_existing=True

)

class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User",foreign_keys=[user_id])
    time = relationship("TimeBooking",secondary=date_table)


booking= Booking.__table__



class TimeBooking(Base):
    __tablename__ = "booking_time"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time)
    is_booking = Column(Boolean, default=True)
    master_confirm = Column(Boolean, default=False)
    phone_owner = Column(String)
    date = relationship("Booking",secondary=date_table)
    booking_id = Column(Integer, ForeignKey("booking.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User",foreign_keys=[owner_id])
    booking = relationship("Booking",foreign_keys=[booking_id])


booking_time= TimeBooking.__table__
