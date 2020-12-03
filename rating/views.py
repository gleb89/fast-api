from fastapi import APIRouter, Depends
from .schemas import RatingBase
from .models import Rating
from .crud import get_rating_by, create_rating_by
from sqlalchemy.orm import Session
from config.db import get_db


rating_router = APIRouter()



@rating_router.get('/rating')
async def create_room(id:int, db: Session = Depends(get_db)):
    """Return rating  user"""
    rating_user = await get_rating_by(id,db)

    return rating_user


@rating_router.post('/rating')
async def create_room(rating:RatingBase, db: Session = Depends(get_db)):
    """Create new update   rating user"""
    user_rating = await create_rating_by(rating,db)
    return user_rating
