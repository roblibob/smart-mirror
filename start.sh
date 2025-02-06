#!/bin/bash
source venv/bin/activate

echo "🚀 Building React UI..."
cd ui || exit 1
npm install
npm run build

echo "✅ React build complete."
cd ..

echo "🎭 Starting Application..."
python main.py &
MAIN_PID=$!

# Trap to clean up processes on exit
cleanup() {
    echo "🛑 Stopping processes..."
    kill $MAIN_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait