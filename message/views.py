from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .crud import ConnectionManager, list_messages_and_rooms, create_chat
import json
from .schemas import RoomCreate
from config.db import  get_db
from fastapi import Depends
from sqlalchemy.orm import Session



chat_router = APIRouter()
manager = ConnectionManager()



@chat_router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int,db: Session = Depends(get_db)):
    """Message websocket and create message in db"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            json_message = json.loads(data)
            message = json_message['text']
            client = json_message['user_id']
            await create_chat(json_message,db)
            # await manager.send_personal_message( json.dumps({'message':message,'user':vv }) , websocket)
            await manager.broadcast(json.dumps({'message':message,'user':client }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client  left the chat")



@chat_router.post('/room-message')
async def create_room(room: RoomCreate,db: Session = Depends(get_db)):
    """Create new room  or return bool room"""
    room_and_messages = await list_messages_and_rooms(room,db)
    return room_and_messages
