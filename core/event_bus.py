import threading
import asyncio
from core.websocket_manager import websocket_manager

class EventBus:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        """Singleton instance creation."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance.listeners = {}
                cls._instance.lock = threading.Lock()
        return cls._instance
    
    def on(self, event_name, callback):
        """Registers a callback for a specific event."""
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(callback)
            print(f"🔊 Registered callback for event: {event_name}")

    def emit(self, event_name, data=None):
        print(f"📡 Emitting event: {event_name}")
        """Triggers all callbacks associated with an event."""
        
        with self.lock:
            listeners = self.listeners.copy()
        if event_name in listeners:
            for callback in listeners[event_name]:
                try:
                    print(f"🔊 Running callback for event: {event_name}")
                    callback(data)
                except Exception as e:
                    print(f"⚠️ Error in event {event_name}: {e}")
        else:
            print(f"⚠️ No listeners found for event: {event_name}")

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