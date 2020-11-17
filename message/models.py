from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, sql
from config.db import Base
from sqlalchemy.orm import relationship, backref




class Room(Base):
    __tablename__ = "rooms"


    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=sql.func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User",foreign_keys=[owner_id])




class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    date = Column(DateTime(timezone=True), server_default=sql.func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

    room = relationship("Room", foreign_keys=[room_id])
    user = relationship("User",foreign_keys=[user_id])






rooms= Room.__table__
chats= Chat.__table__
