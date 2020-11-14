from fastapi import FastAPI, Request, Response, Depends, Cookie,Header,Form
from config.base import Base
from config.db import engine
from config.db import SessionLocal
from users_profile import views
from message.views import routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',tags=["templates"])
def hh(request: Request):
    return templates.TemplateResponse("home.html", {"request": request,})

@app.get('/login',tags=["templates"])
def hh(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,})


@app.get('/item',tags=["templates"])
def hh(request: Request):
    return templates.TemplateResponse("items.html", {"request": request,})

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
