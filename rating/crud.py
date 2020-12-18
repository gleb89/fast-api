from .models import Rating
from users_profile import models




async def create_rating_by(rating,db):
    owner_rating = db.query(Rating).filter(Rating.user_id == rating.user_id, Rating.owner_id == rating.owner_id).first()
    user = db.query(models.User).filter(models.User.id == rating.user_id ).first()
    if owner_rating:
        update_rating =  db.query(Rating).filter(Rating.user_id == rating.user_id,Rating.owner_id == rating.owner_id).update\
                                                    (dict(rating=rating.rating))
        db.commit()
        rating_user = await get_rating_by(rating.user_id,db)
        return {'rating_user':rating_user}
    else:
        new_rating = Rating(user_id=rating.user_id,owner_id=rating.owner_id,rating=rating.rating)

        user.children.append(new_rating)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        rating_user = await get_rating_by(rating.user_id,db)
        return {'rating_user':rating_user}




async def  get_rating_by(id,db):
    rating = db.query(Rating).filter(Rating.user_id == id ).all()
    rating_user = 0
    list_rating = []
    for i in rating:
        list_rating.append(i)
        rating_user += i.rating
    rating_items = len(list_rating)
    if rating_user != 0:
        rating_user = round(rating_user/rating_items)
    else:
        rating_user = round(0)
    return {'rating':rating,'rating_user':rating_user}