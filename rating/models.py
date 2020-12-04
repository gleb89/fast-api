from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from config.db import Base
from sqlalchemy.orm import relationship
from config.db import get_db
from .schemas import UserRating

rating_table = Table('association', Base.metadata,
    Column('users', Integer, ForeignKey('users.id')),
    Column('rating', Integer, ForeignKey('rating.id'))

)

class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer,default=0)
    owner_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User",foreign_keys=[user_id])
    owner = relationship("User",foreign_keys=[owner_id])






# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Child",
#                     secondary=rating_table)

# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)

# p = Parent()
# a = Child()
# p.children.append(a)

# for assoc in p.children:
#     print(assoc)
