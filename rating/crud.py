from .models import Rating



async def create_rating_by(rating,db):
    owner_rating = db.query(Rating).filter(Rating.user_id == rating.user_id, Rating.owner_id == rating.owner_id).first()

    if owner_rating:
        update_rating =  db.query(Rating).filter(Rating.user_id == rating.user_id,Rating.owner_id == rating.owner_id).update\
                                                    (dict(rating=rating.rating))
        rating_user = await get_rating_by(rating.user_id,db)
        return {'rating_user':rating_user}
    else:
        new_rating = Rating(user_id=rating.user_id,owner_id=rating.owner_id,rating=rating.rating)
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
    print(rating_user)
    rating_user = rating_user/rating_items
    return {'rating':rating,'rating_user':rating_user}