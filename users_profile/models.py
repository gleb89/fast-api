from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from config.db import Base
from sqlalchemy.orm import relationship
from rating.models import rating_table

images_table = Table('images_user', Base.metadata,
    Column('users', Integer, ForeignKey('users.id')),
    Column('images', Integer, ForeignKey('images.id')
    ),
    extend_existing=True

)

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    city = Column(String)
    avatar = Column( String(100))
    phone = Column(String(100))
    is_active = Column(Boolean, default=True)
    master = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship("Category",foreign_keys=[category_id])
    children = relationship("Rating",secondary=rating_table)
    images = relationship("Images",secondary=images_table)

    @property
    def bb(self):
        rating = 0
        count_rating = []
        for num_rating in self.children:
            rating += num_rating.rating
            count_rating.append(num_rating)
        count_rating = len(count_rating)
        if rating != 0:
            return round(rating/count_rating)
        else:
            return round(rating)



class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    images = Column( String(100))

    user = relationship("User",foreign_keys=[user_id])


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)





users = User.__table__