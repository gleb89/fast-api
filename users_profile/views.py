from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, status, File, UploadFile
from sqlalchemy.orm import Session
from config.db import get_db
from . import crud, models, schemas
from .crud import create_access_token,authenticate_user,get_current_active_user, image_add
from datetime import timedelta
from users_profile.schemas import Token



user_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30



@user_router.post("/token", response_model=Token)
def login_for_access_token(form_data:schemas.UserLogin ,db: Session = Depends(get_db)):
    """Return jwt token,authorization"""
    user = authenticate_user(db , form_data.name, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@user_router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    """Return user in auth"""
    return current_user



@user_router.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(get_current_active_user),users:schemas.UsId= Depends(crud.user_all)):
    """return user and user all"""
    users = list(users)
    return [{"item_id": "Foo", "user": current_user,'users_all':users}]



@user_router.post("/user", response_model=schemas.UserInfo)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registration user"""
    db_user =   await crud.get_user_by_username(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return  crud.create_user(db=db, user=user)



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
async def image_add_user(user_id:int,image: UploadFile = File(...),db: Session = Depends(get_db)):
    """User image avatar add"""
    avatar = await image_add(image,user_id,db)
    return avatar
