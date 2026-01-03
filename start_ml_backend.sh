#!/bin/bash
# Start ML Service and Backend together

echo "🚀 Starting AdGenesis Services..."
echo ""

# Check if ML service is already running
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  ML Service already running on port 8001"
else
    echo "🤖 Starting ML Service (port 8001)..."
    cd ml_pipeline
    python serve_design.py &
    ML_PID=$!
    echo "   ML Service PID: $ML_PID"
    cd ..
fi

# Wait for ML service to initialize
echo "⏳ Waiting for ML service to load model..."
sleep 5

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Backend already running on port 8000"
else
    echo "🔧 Starting Backend API (port 8000)..."
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    echo "   Backend PID: $BACKEND_PID"
    cd ..
fi

echo ""
echo "✅ Services started!"
echo ""
echo "📊 Service URLs:"
echo "   ML Service:    http://localhost:8001"
echo "   Backend API:   http://localhost:8000"
echo "   API Docs:      http://localhost:8000/docs"
echo ""
echo "🧪 Test the model:"
echo "   cd ml_pipeline && python client.py"
echo ""
echo "🛑 To stop services:"
echo "   pkill -f serve_design.py"
echo "   pkill -f uvicorn"
echo ""
