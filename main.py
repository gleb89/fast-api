from fastapi import FastAPI, Request, Response
from config.base import Base
from config.db import engine
from config.db import SessionLocal
from users_profile.views import user_router
from message.views import chat_router
from templates.views import templates_router
from booking.views  import booking_router
from rating.views  import rating_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "https://new-nuxtjs.herokuapp.com"
]



@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#apps routers include
app.include_router(user_router, tags=["users"])
app.include_router(chat_router, tags=["messages and room"])
app.include_router(templates_router, tags=["Templates"])
app.include_router(booking_router, tags=["booking"])
app.include_router(rating_router, tags=["rating"])


Base.metadata.create_all(bind=engine)
