from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    avatar = Column( String(100))
    is_active = Column(Boolean, default=True)



users = User.__table__