#!/bin/bash
# Quick Commands - AdGenesis Post-Training

echo "🎨 AdGenesis - Quick Command Reference"
echo "======================================"
echo ""

show_help() {
    echo "Available commands:"
    echo ""
    echo "  ./commands.sh start      - Start ML + Backend services"
    echo "  ./commands.sh test       - Run integration tests"
    echo "  ./commands.sh stop       - Stop all services"
    echo "  ./commands.sh status     - Check service status"
    echo "  ./commands.sh logs       - Show service logs"
    echo "  ./commands.sh frontend   - Start frontend dev server"
    echo "  ./commands.sh help       - Show this help"
    echo ""
}

start_services() {
    echo "🚀 Starting services..."
    ./start_ml_backend.sh
}

test_integration() {
    echo "🧪 Running integration tests..."
    python test_integration.py
}

stop_services() {
    echo "🛑 Stopping services..."
    pkill -f serve_design.py && echo "   Stopped ML service"
    pkill -f uvicorn && echo "   Stopped backend"
    echo "✅ All services stopped"
}

check_status() {
    echo "📊 Service Status:"
    echo ""
    
    if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ ML Service (8001):    RUNNING"
    else
        echo "❌ ML Service (8001):    STOPPED"
    fi
    
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ Backend API (8000):   RUNNING"
    else
        echo "❌ Backend API (8000):   STOPPED"
    fi
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ Frontend (3000):      RUNNING"
    else
        echo "❌ Frontend (3000):      STOPPED"
    fi
}

show_logs() {
    echo "📝 Recent logs:"
    echo ""
    echo "=== ML Service ==="
    if [ -f ml_pipeline/serve_design.log ]; then
        tail -20 ml_pipeline/serve_design.log
    else
        echo "No logs found"
    fi
    echo ""
    echo "=== Backend ==="
    if [ -f backend/backend.log ]; then
        tail -20 backend/backend.log
    else
        echo "No logs found"
    fi
}

start_frontend() {
    echo "🎨 Starting frontend..."
    cd frontend
    npm start
}

# Main command router
case "$1" in
    start)
        start_services
        ;;
    test)
        test_integration
        ;;
    stop)
        stop_services
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    frontend)
        start_frontend
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
