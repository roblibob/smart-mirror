import threading
import asyncio
from core.websocket_manager import websocket_manager

class EventBus:
    def __init__(self):
        self.listeners = {}
        self.lock = threading.Lock()

    def on(self, event_name, callback):
        """Registers a callback for a specific event."""
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(callback)

    def emit(self, event_name, data=None):
        """Triggers all callbacks associated with an event."""
        with self.lock:
            if event_name in self.listeners:
                for callback in self.listeners[event_name]:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"⚠️ Error in event {event_name}: {e}")

        # Push event to frontend via WebSockets
        event_data = {"event": event_name, "data": data}
        self._safe_broadcast(event_data)

    def _safe_broadcast(self, event_data):
        """Ensures the WebSocket broadcast runs in an event loop."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(websocket_manager.broadcast(event_data))
        except RuntimeError:
            # No running loop, start one in a separate thread
            asyncio.run(self._broadcast(event_data))

    async def _broadcast(self, event_data):
        """Async broadcast method to send data to WebSockets."""
        await websocket_manager.broadcast(event_data)

    def off(self, event_name, callback):
        """Removes a specific callback from an event."""
        with self.lock:
            if event_name in self.listeners:
                self.listeners[event_name].remove(callback)
                if not self.listeners[event_name]:  # Cleanup if empty
                    del self.listeners[event_name]

# Create a global instance of the event bus
event_bus = EventBus()