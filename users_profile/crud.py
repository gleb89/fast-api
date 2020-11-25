from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Response, Depends,HTTPException, status
from fastapi.responses import JSONResponse
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer
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
import shutil




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




#registrations
async def get_user_by_username(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

get_user_by_username


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password.encode('utf-8'))
    db_user = models.User(name=user.name,password=hashed_password,email = user.email,city = user.city)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



#login asses tocken views
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


TokenData
def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(db, email: str):
    users_db = db.query(models.User).all()
    for users in users_db:
        if email == users.email:

            user_dict = db.query(models.User).filter\
                    (models.User.email == email).first()
            return UserAuthenticate(name=user_dict.name,\
                            password=user_dict.password,id=user_dict.id,email=user_dict.email)



def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(current_user: schemas.User = Depends\
                                                    (get_current_user)):
    return current_user

get_user_by_username

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

authenticate_user

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



async def image_add(image,user_id,db):
    with open(f"static/images/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        avatar = f'https://glebhleb.herokuapp.com/static/images/{image.filename}'
        user =  db.query(models.User).filter(models.User.id == user_id).update\
                                                    (dict(avatar=avatar))
        db.commit()
    return avatar
