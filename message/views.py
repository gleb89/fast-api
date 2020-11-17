from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .crud import ConnectionManager
import json
from .schemas import RoomCreate
from config.db import  get_db
from fastapi import Depends
from .models import Room
from sqlalchemy.orm import Session


routers = APIRouter()
manager = ConnectionManager()



#message
@routers.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            json_message = json.loads(data)
            message = json_message['mess']
            client = json_message['user']
            # await manager.send_personal_message( json.dumps({'message':message,'user':vv }) , websocket)
            await manager.broadcast(json.dumps({'message':message,'user':client }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client  left the chat")

@routers.post('/newmessage')
def create_user(room: RoomCreate,db: Session = Depends(get_db)):
    room = Room(owner_id=room.owner_id,date=room.date)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
