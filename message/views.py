from fastapi import APIRouter, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.authentication import requires

routers = APIRouter()
templates = Jinja2Templates(directory="templates")

# @routers.get('/bbb')
# def home():
#     return {'hh':'jj'}


# @routers.get("/",response_class=HTMLResponse)
# async def get(request:Request):

#     return templates.TemplateResponse('index.html',{"request": request})


# @routers.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):

#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")