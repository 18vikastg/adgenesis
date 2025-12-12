#!/bin/bash

# AdGenesis - Complete Startup Script
# Run this to start all services

echo "🚀 Starting AdGenesis Services..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists
if [ ! -d "$DIR/backend/venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Creating virtual environment..."
    cd "$DIR/backend"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd "$DIR"
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    lsof -ti:8001 | xargs kill -9 2>/dev/null || true
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Kill any existing services
echo "🧹 Cleaning up existing services..."
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
sleep 2

# Start ML Service
echo -e "${BLUE}🤖 Starting ML Service on port 8001...${NC}"
cd "$DIR/ml_pipeline"
nohup python serve.py --model gpt2 > /tmp/ml_service.log 2>&1 &
ML_PID=$!
sleep 5

# Check if ML service started (check if port is listening)
if lsof -i:8001 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ ML Service running (PID: $ML_PID)${NC}"
else
    echo -e "${RED}❌ ML Service failed to start. Check /tmp/ml_service.log${NC}"
    tail -20 /tmp/ml_service.log
    exit 1
fi

# Start Backend
echo -e "${BLUE}🔧 Starting Backend on port 8000...${NC}"
cd "$DIR/backend"
source venv/bin/activate
nohup uvicorn app.main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 5

# Check if backend started
if lsof -i:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ Backend failed to start. Check /tmp/backend.log${NC}"
    tail -20 /tmp/backend.log
    exit 1
fi

# Start Frontend
echo -e "${BLUE}🎨 Starting Frontend on port 3000...${NC}"
cd "$DIR/frontend"
nohup npm start > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 15

# Check if frontend started
if lsof -i:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend running (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}❌ Frontend failed to start. Check /tmp/frontend.log${NC}"
    tail -20 /tmp/frontend.log
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════"
echo -e "${GREEN}✨ All services are running!${NC}"
echo "═══════════════════════════════════════════════"
echo ""
echo "🤖 ML Service:  http://localhost:8001"
echo "🔧 Backend:     http://localhost:8000"
echo "🎨 Frontend:    http://localhost:3000"
echo ""
echo "📝 Logs:"
echo "   ML:       tail -f /tmp/ml_service.log"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
while true; do
    sleep 1
done
