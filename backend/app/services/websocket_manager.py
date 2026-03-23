# -*- coding: utf-8 -*-
"""
GIMAT — WebSocket Manager
Handles real-time data broadcasting to connected frontend clients
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, event_type: str, data: dict):
        """
        Broadcast a message to all connected clients.
        event_type options: "new_data", "new_alert", "station_updated"
        """
        message = json.dumps({"type": event_type, "payload": data})
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)
        
        # Cleanup broken connections
        for conn in disconnected:
            self.disconnect(conn)

# Global manager instance
manager = ConnectionManager()
