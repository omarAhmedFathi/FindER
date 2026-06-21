from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import json
import logging

router = APIRouter(prefix="/ws", tags=["websocket"])
logger = logging.getLogger("websocket")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.chat_rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if room_id:
            if room_id not in self.chat_rooms:
                self.chat_rooms[room_id] = []
            self.chat_rooms[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if room_id and room_id in self.chat_rooms:
            if websocket in self.chat_rooms[room_id]:
                self.chat_rooms[room_id].remove(websocket)

    async def broadcast(self, message: str, room_id: str = None):
        targets = self.chat_rooms.get(room_id, []) if room_id else self.active_connections
        for connection in targets:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"WS send error: {str(e)}")

manager = ConnectionManager()

@router.websocket("/live-dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/chat/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast incoming chat message to everyone in the room
            await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
