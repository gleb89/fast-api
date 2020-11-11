from fastapi import APIRouter
from users_profile import  views

routes = APIRouter()

routes.include_router(views.router, prefix="/users")