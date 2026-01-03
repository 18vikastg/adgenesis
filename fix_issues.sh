#!/bin/bash
# Setup script to fix common issues

echo "🔧 AdGenesis - Issue Fixer"
echo "=========================="
echo ""

# Fix 1: Repository doesn't exist on GitHub yet
echo "📦 Git Repository Setup"
echo "------------------------"
echo ""
echo "The repository 'https://github.com/18vikastg/adgenesis.git' doesn't exist yet."
echo ""
echo "OPTIONS:"
echo ""
echo "1️⃣  Create the repository on GitHub:"
echo "   • Go to https://github.com/new"
echo "   • Repository name: adgenesis"
echo "   • Make it Public or Private"
echo "   • Don't initialize with README (we already have code)"
echo "   • Click 'Create repository'"
echo ""
echo "2️⃣  Then push your code:"
echo "   cd /home/vikas/Desktop/adgenesis"
echo "   git push -u origin main"
echo ""
echo "3️⃣  OR work without GitHub for now:"
echo "   # Remove the remote"
echo "   git remote remove origin"
echo ""
echo "   # Work locally, push later when repo is created"
echo ""

# Fix 2: Check if ML service is running
echo ""
echo "🤖 Checking ML Service..."
echo "------------------------"
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ ML Service is running"
else
    echo "❌ ML Service is NOT running"
    echo ""
    echo "Start it with:"
    echo "  cd /home/vikas/Desktop/adgenesis/ml_pipeline"
    echo "  python serve_design.py"
fi

# Fix 3: Check if backend is running
echo ""
echo "🔧 Checking Backend API..."
echo "------------------------"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API is NOT running"
    echo ""
    echo "Start it with:"
    echo "  cd /home/vikas/Desktop/adgenesis/backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
fi

echo ""
echo "✅ client.py has been fixed - no more /models endpoint error"
echo ""
