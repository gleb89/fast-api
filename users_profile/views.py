from typing import List
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, APIRouter, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from config.db import get_db
from . import crud, models, schemas
from config.db import SessionLocal, engine
from . import  models
from .crud import create_access_token,authenticate_user,get_current_active_user
from datetime import timedelta
from users_profile.schemas import Token
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from  users_profile.email import conf
from  starlette.responses  import  JSONResponse
import smtplib



router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data:schemas.UserLogin ,db: Session = Depends(get_db)):
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



@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user



@router.get("/users/me/items/")
async def read_own_items(current_user: models.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.name}]



@router.post("/user", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)



#send email password
@router.post('/send_email')
async def email(email:schemas.EmailSchema, db: Session = Depends(get_db)):
    send_message = crud.get_user_by_email(db,email)
    return send_message



#user password update
@router.put('/reset_password')
async def reset_password(form_password:schemas.EmailRessetPassword,db: Session = Depends(get_db)):
    new_password = crud.reset_user_password(form_password,db)
    return new_password
