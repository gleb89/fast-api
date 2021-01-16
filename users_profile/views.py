from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db
from . import crud, models, schemas
from .crud import create_access_token,authenticate_user,get_current_active_user,\
                        image_add, user_by_login, add_category, reset_user_data,\
                                    categories_db, images_add_album, images_delete
from datetime import timedelta
from users_profile.schemas import Token



user_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@user_router.post("/categories")
async def create_category(categories: schemas.Category, db: Session = Depends(get_db)):

    """Create Category """
    category = await add_category(categories, db)

    return category


@user_router.get("/categories/")
async def categories_in_db(db: Session = Depends(get_db)):

    """Return categories all """
    categories = await crud.categories_db(db)
    return categories

@user_router.post("/token", response_model=Token)
def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):

    """Return jwt token,authorization for docs panel"""
    user = authenticate_user(db , form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@user_router.post("/login")
def login_for_access_token(form_data:schemas.UserLogin ,db: Session = Depends(get_db)):

    """Return jwt token,authorization"""
    user = authenticate_user(db , form_data.email, form_data.password)
    user_login = user_by_login(db,form_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",'user':user_login}





@user_router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):

    """Return user in auth items"""
    return current_user



@user_router.get("/users")
async def read_own_items(db: Session = Depends(get_db)):

    """return user all"""
    users = await crud.user_all(db)
    return {'users':users}




@user_router.post("/user")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    """Registration user"""
    db_user =   await crud.get_user_by_username(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Такой email существует")
    return  crud.create_user(db=db, user=user)


@user_router.get("/user/{id}")
async def user_in_db(id:int, db: Session = Depends(get_db)):

    """Return user == id in db """
    user = await crud.user_db(id,db)
    return user


@user_router.put('/reset_user')
async def reset_user(user_data:schemas.UserUpdate, db: Session = Depends(get_db)):
    """User password update"""
    user = await crud.reset_user_data(user_data,db)
    return user

@user_router.post('/send_email')
async def email(email:schemas.EmailSchema, db: Session = Depends(get_db)):

    """Send email password(reset)"""
    send_message = crud.get_user_by_email(db,email)
    return send_message



@user_router.put('/reset_password')
async def reset_password(form_password:schemas.EmailRessetPassword,db: Session = Depends(get_db)):
    """User password update"""
    new_password = crud.reset_user_password(form_password,db)
    return new_password


@user_router.put('/add-image/{user_id}')
async def image_add_user(user_id:int,image:UploadFile = File(...),db: Session = Depends(get_db)):

    """User image avatar add"""
    new_image = await image_add(image, user_id,db)
    return new_image




@user_router.post('/add-images/{user_id}')
async def images_add(user_id:int,image:UploadFile = File(...),db: Session = Depends(get_db)):

    """User image album add"""
    new_image = await images_add_album(image, user_id,db)
    return new_image


@user_router.delete('/del-images/{image_id}')
async def images_add(image_id:int,user_id:int, db: Session = Depends(get_db)):

    """User image album add"""
    del_image = await images_delete(image_id, user_id, db)
    return del_image