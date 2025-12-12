#!/bin/bash
# ADGENESIS - Start all services

set -e

echo "🚀 Starting ADGENESIS Services"
echo "================================"

# Change to project directory
cd "$(dirname "$0")"

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
sleep 5

# Check ML service health
if curl -s http://localhost:8001/ > /dev/null; then
    echo "✅ ML service is healthy"
else
    echo "❌ ML service failed to start. Check /tmp/ml_service.log"
    exit 1
fi

# Start backend
echo "🔧 Starting backend on port 8000..."
cd backend
uvicorn app.main:app --reload --port 8000
