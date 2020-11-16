from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Response, Depends,HTTPException, status
from fastapi.responses import JSONResponse
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import bcrypt
from config.db import SECRET_KEY, ALGORITHM
from datetime import timedelta
from datetime import datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from .schemas import UserAuthenticate,TokenData
from typing import Optional
from config.db import get_db
import smtplib
import asyncio



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



#registrations
async def get_user_by_username(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()



def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password.encode('utf-8'))
    db_user = models.User(name=user.name,password=hashed_password,\
                                                    email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



#login asses tocken views
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(db, name: str):
    users_db = db.query(models.User).all()
    for users in users_db:

        if name in users.name:
            user_dict = db.query(models.User).filter\
                    (models.User.name == name).first()
            return UserAuthenticate(name=user_dict.name,\
                            password=user_dict.password)



def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)

    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme),\
                            db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except JWTError:
        raise credentials_exception
    user = get_user(db, name=token_data.name)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(current_user: schemas.User = Depends\
                                                    (get_current_user)):
    return current_user



def get_user_by_email(db, email: schemas.EmailSchema):
    user =  db.query(models.User).filter(models.User.email == email.email).first()
    if user:
        message = 'для востановления пароля перейдите по ссылке\
                http://127.0.0.1:8000/reset_password'.encode('utf-8')
        server = smtplib.SMTP('smtp.mail.ru',587)
        server.starttls()
        server.login('beautyroom37@mail.ru', 'Kit241281')
        server.sendmail('beautyroom37@mail.ru',email.email,message)
        server.close()
        print('kk')
        return {'message':f'password sent email {email.email}'}
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,\
                                content={'message':'incorrect email'})



def reset_user_password(form_pasword,db):
    hashed_password = pwd_context.hash(form_pasword.password .encode('utf-8'))
    user =  db.query(models.User).filter\
            (models.User.email == form_pasword.email).update\
                            (dict(password=hashed_password))

    if user:
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK,content={'message':'пароль успешно изменене'})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,\
                         content={'message':'Неверно введен email'})


def user_all(db: Session = Depends(get_db)):
    users =  db.query(models.User).all()
    return users
