#!/bin/bash
source venv/bin/activate

echo "🚀 Building React UI..."
cd ui || exit 1
npm install
npm run build

echo "✅ React build complete."

echo "🔄 Starting Electron..."
npm start &
ELECTRON_PID=$!
cd ..

echo "🔄 Starting API..."
uvicorn api.main:app --host 127.0.0.1 --port 8000 &
API_PID=$!

echo "🎭 Starting Face Recognition..."
python3 main.py &
MAIN_PID=$!

# Trap to clean up processes on exit
cleanup() {
    echo "🛑 Stopping processes..."
    kill $ELECTRON_PID $API_PID $MAIN_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait