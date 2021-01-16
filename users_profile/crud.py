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
from .schemas import UsId
import os





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




#registrations
async def get_user_by_username(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

async def add_category(category,db):
    category = models.Category(title=category.title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


async def categories_db(db):
    categories = db.query(models.Category).all()
    return categories

async def reset_user_data(user_data, db):
    category = db.query(models.Category).filter(models.Category.id == user_data.category)
    user =  db.query(models.User).filter(models.User.id == user_data.id).update\
                                    (dict(name=user_data.name,city = user_data.city,\
                                email = user_data.email,category_id = user_data.category, phone = user_data.phone))

    db.commit()
    user = db.query(models.User).filter(models.User.id == user_data.id).first()

    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password.encode('utf-8'))

    if user.category_id != 0:
        category = db.query(models.Category).filter(models.Category.id == user.category_id)
        db_user = models.User(name=user.name,password=hashed_password,email = user.email,\
                                                city = user.city,master = user.master,\
                                                avatar = '',category_id = user.category_id,\
                                                phone = user.phone)
    else:

        db_user = models.User(name=user.name,password=hashed_password,email = user.email,city = user.city,master = user.master,avatar = '')

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



#login asses tocken views
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(db, email: str):
    users_db = db.query(models.User).all()
    for users in users_db:
        if email == users.email:

            user_dict = db.query(models.User).filter\
                    (models.User.email == email).first()
            return UserAuthenticate(name=user_dict.name,\
                            password=user_dict.password,id=user_dict.id,email=user_dict.email,master = user_dict.master)



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

async def user_db(id,db):
    user =  db.query(models.User).filter(models.User.id == id).first()
    print(user.bb)
    user_schema = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "master": user.master,
        "city": user.city,
        "avatar": user.avatar,
        "rating":user.bb,
        "category":user.category,
        "images":user.images,
        "phone":user.phone
    }


    return user_schema

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



async def get_current_active_user(current_user: schemas.UserInfo = Depends\
                                                    (get_current_user)):
    return current_user



def user_by_login(db,email):
    user =  db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user
    else:
        return None


def get_user_by_email(db, email: schemas.EmailSchema):
    user =  db.query(models.User).filter(models.User.email == email.email).first()
    if user:
        message = 'для востановления пароля перейдите по ссылке\
                http://127.0.0.1:8000/reset_password'.encode('utf-8')
        server = smtplib.SMTP('smtp.mail.ru',587)
        server.starttls()
        server.login('beautyroom37@mail.ru','Polina072020' )
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



async def rati(users):
    list_user = []
    for user in users:
        user_schema = {
        "email": user.email,
        "id": user.id,
        "master": user.master,
        "avatar": user.avatar,
        "name": user.name,
        "is_active": user.is_active,
        "city": user.city,
        "children": user.children,
        "rating":user.bb,
        "category":user.category,
        'images':user.images,
        'phone':user.phone
        }
        list_user.append(user_schema)
    return list_user


from rating.models import Rating
from sqlalchemy import func

async def user_all(db):
    users =  db.query(models.User).filter(models.User.master == True).all()
    list_users = await rati(users)
    users_rating = [i.children for i in users]
    users_images = [i.images for i in users]
    return list_users






async def image_add(image,user_id,db):
    with open(f"static/images/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        avatar = f'https://glebhleb.herokuapp.com/static/images/{image.filename}'
        user =  db.query(models.User).filter(models.User.id == user_id).update\
                                                    (dict(avatar=avatar))
        db.commit()
    return avatar

create_user
async def images_add_album(image,user_id,db):
    user =  db.query(models.User).filter(models.User.id == user_id).first()
    with open(f"static/images/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        images = f'https://glebhleb.herokuapp.com/static/images/{image.filename}'
        new_images = models.Images(user_id=user_id,images = images)
        db.add(new_images)
        db.commit()
        db.refresh(new_images)
        user.images.append(new_images)
        db.commit()
        db.refresh(new_images)
    return new_images


async def images_delete(image_id,user_id,db):
    user = db.query(models.User).get(user_id)
    
    image = db.query(models.Images).filter(models.Images.id == image_id).first()
    user.images.remove(image )
    image_name = image.images[45:]
    db.commit()
    os.remove(f"./static/images/{image_name}")
    

    return JSONResponse(status_code=200, content={'message': "image delete"})





