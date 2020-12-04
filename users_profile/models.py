from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship
from rating.models import rating_table



class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    city = Column(String)
    avatar = Column( String(100))
    is_active = Column(Boolean, default=True)
    master = Column(Boolean, default=False)
    children = relationship("Rating",secondary=rating_table)



    @property
    def bb(self):
        rating = 0
        count_rating = []
        for num_rating in self.children:
            rating += num_rating.rating
            count_rating.append(num_rating)
        count_rating = len(count_rating)
        if rating != 0:
            return rating/count_rating
        else:
            return rating

users = User.__table__