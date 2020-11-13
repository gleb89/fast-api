from fastapi import FastAPI, Request, Response, Depends, Cookie,Header,Form
from config.base import Base
from config.db import engine
from config.db import SessionLocal
from users_profile import views
from message.views import routers

from typing import Optional
from pydantic import BaseModel

app = FastAPI()



@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(views.router)
app.include_router(routers)

Base.metadata.create_all(bind=engine)
