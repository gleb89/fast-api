import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()



# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = 'ururuirjfmfmf'

ALGORITHM = "HS256"
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@db:5432/{DB}"






engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


