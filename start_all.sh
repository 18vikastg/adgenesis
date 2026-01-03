#!/bin/bash
# Ultimate Quick Start Script

echo "🎨 AdGenesis - Complete Startup"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if ML service is running
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✅ ML Service already running${NC}"
else
    echo "🤖 Starting ML Service..."
    cd /home/vikas/Desktop/adgenesis/ml_pipeline
    nohup python serve_design.py > ml_service.log 2>&1 &
    echo "   PID: $!"
    cd ..
    sleep 3
fi

# Check if backend is running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend already running${NC}"
else
    echo "🔧 Starting Backend..."
    cd /home/vikas/Desktop/adgenesis/backend
    source venv/bin/activate
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    echo "   PID: $!"
    cd ..
    sleep 2
fi

# Check if frontend is running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend already running${NC}"
else
    echo "🎨 Starting Frontend..."
    cd /home/vikas/Desktop/adgenesis/frontend
    npm start &
    echo "   Starting..."
    cd ..
fi

echo ""
echo "================================"
echo -e "${GREEN}✅ All services started!${NC}"
echo "================================"
echo ""
echo "📊 Your Application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   ML Service: http://localhost:8001"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🧪 Test the model:"
echo "   cd ml_pipeline && python client.py"
echo ""
echo "🛑 Stop all services:"
echo "   pkill -f serve_design.py"
echo "   pkill -f uvicorn"
echo "   pkill -f 'npm start'"
echo ""
