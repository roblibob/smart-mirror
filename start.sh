#!/bin/bash

echo "Starting Smart Mirror..."

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server in the background
echo "Starting FastAPI..."

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Start face detection script in the background
echo "Starting Face Recognition..."
python main.py &
FACE_PID=$!

# Start Electron UI in the background
echo "Starting Electron UI..."
cd ui
npm start &
ELECTRON_PID=$!
cd ..

# Function to stop all processes
cleanup() {
    echo "Stopping Smart Mirror..."
    kill $API_PID $FACE_PID $ELECTRON_PID
    exit 0
}

# Trap exit signals and call cleanup()
trap cleanup SIGINT SIGTERM

# Keep script running until stopped
wait