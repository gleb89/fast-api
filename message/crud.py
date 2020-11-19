from fastapi import WebSocket
from .models import Room, Chat
from .schemas import  ChatCreate



class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message):
        for connection in self.active_connections:
                await connection.send_text(message)



async def list_messages_and_rooms(room,db):
    room_bool = db.query(Room).filter(Room.owner_id == room.owner_id,Room.invited_id==room.invited_id).first()
    if room_bool :
        message_room = db.query(Chat).filter(Chat.room_id == room_bool.id ).all()
        return {'room':room_bool,'messages':message_room}
    else:
        new_room = Room(owner_id=room.owner_id,invited_id=room.invited_id,date=room.date)
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        return new_room


async def create_chat(chat:ChatCreate,db):
    chat = Chat(user_id=int(chat['user_id']),room_id=chat['room_id'],text=chat['text'],date=chat['date'])
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat