from fastapi import FastAPI, Response, APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


templates_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@templates_router.get('/')
def home(request: Request):
    return RedirectResponse("/docs")



@templates_router.get('/login')
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,})




@templates_router.get('/item')
def item(request: Request):
    return templates.TemplateResponse("items.html", {"request": request,})


@templates_router.get('/message')
def sendmessage(request: Request):
    return templates.TemplateResponse("message.html", {"request": request,})


@templates_router.get('/mess')
def sendmessage(request: Request):
    return templates.TemplateResponse("rer.html", {"request": request,})
