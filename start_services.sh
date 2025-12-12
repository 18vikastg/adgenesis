#!/bin/bash
# ADGENESIS - Start all services

set -e

echo "🚀 Starting ADGENESIS Services"
echo "================================"

# Change to project directory
cd "$(dirname "$0")"

# Kill any existing services
echo "🧹 Cleaning up existing services..."
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Activate virtual environment
echo "📦 Activating virtual environment..."
source backend/venv/bin/activate

# Start ML service in background
echo "🤖 Starting ML service on port 8001..."
cd ml_pipeline
nohup python serve.py --model gpt2 > /tmp/ml_service.log 2>&1 &
ML_PID=$!
echo "   ML service PID: $ML_PID"
cd ..

# Wait for ML service to start
echo "⏳ Waiting for ML service to initialize..."
for i in {1..15}; do
    if curl -s http://localhost:8001/ > /dev/null 2>&1; then
        echo "✅ ML service is healthy"
        break
    fi
    if [ $i -eq 15 ]; then
        echo "❌ ML service failed to start. Check /tmp/ml_service.log"
        cat /tmp/ml_service.log
        exit 1
    fi
    sleep 2
done

# Start backend
echo "🔧 Starting backend on port 8000..."
echo ""
echo "📝 Backend will start now. Press Ctrl+C to stop all services."
echo ""
cd backend
uvicorn app.main:app --reload --port 8000
