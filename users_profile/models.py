from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    # room_id =  Column(Integer, ForeignKey("rooms.id"))

    # room = relationship("Room",foreign_keys="[Room.billing_address_id]")

    # user_room = relationship("Room", back_populates="owner")
    # user_room = relationship("Room", back_populates="owner")
    # chat = relationship("Chat", back_populates="user")



users = User.__table__