from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship


class Rating(Base):
    __tablename__ = "rating"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer,default=0)
    owner_id = Column(Integer, ForeignKey('users.id'))


    user = relationship("User",foreign_keys=[user_id])
    owner = relationship("User",foreign_keys=[owner_id])
