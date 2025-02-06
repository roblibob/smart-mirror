import subprocess
import time
import threading
import signal
from core.module_loader import modules  # Load modules
from core.event_bus import event_bus  # Global event bus
from fastapi import FastAPI, WebSocket
from core.websocket_manager import websocket_manager
import uvicorn

RUNNING = True  # Control loop execution
electron_process = None  # Store Electron process
app = FastAPI()

def start_electron():
    """Starts the Electron UI in a separate thread."""
    def run():
        global electron_process
        try:
            electron_process = subprocess.Popen(["npm", "run", "dev"], cwd="ui")
            print("✅ Electron UI started.")
            electron_process.wait()  # Wait for Electron to exit before returning
        except Exception as e:
            print(f"⚠️ Error starting Electron: {e}")

    electron_thread = threading.Thread(target=run, daemon=True)
    electron_thread.start()

def start_fastapi():
    """Starts FastAPI server in a separate thread."""
    def run():
        uvicorn.run(app, host="0.0.0.0", port=8000)

    api_thread = threading.Thread(target=run, daemon=True)
    api_thread.start()

def update_loop():
    """ Continuously updates all modules in separate threads. """
    while RUNNING:
        for name, module in modules.items():
            try:
                module.run_update()
            except Exception as e:
                print(f"⚠️ Error updating module {name}: {e}")

        time.sleep(1)  # Adjust update interval as needed

def handle_shutdown(sig, frame):
    """ Gracefully handles shutdown (Ctrl+C). """
    global RUNNING
    RUNNING = False
    print("\n🛑 Shutting down...")
    time.sleep(1)  # Allow cleanup
    exit(0)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections from frontend clients."""
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive (or process messages)
    except:
        websocket_manager.disconnect(websocket)

# Start Electron
start_electron()

# Start FastAPI server
start_fastapi()

# Attach signal handler for Ctrl+C
signal.signal(signal.SIGINT, handle_shutdown)

# Start the update loop in a separate thread
print("🚀 Starting update loop thread...")
update_thread = threading.Thread(target=update_loop, daemon=True)
update_thread.start()

print("✅ Smart Mirror Update Engine Running...")
update_thread.join()  # Keep the main thread alive