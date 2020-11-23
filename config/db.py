from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = "postgres://cczlittcvwxubo:2b0857467f254162be97df83fffba2c9802a177450c0b2928ba1dcf6d7d22891@ec2-54-247-118-139.eu-west-1.compute.amazonaws.com:5432/df42acu48q6lbm"


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