#!/bin/bash
# Setup script for ML pipeline

set -e

echo "🚀 ADGENESIS ML Pipeline Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "📁 Creating models directory..."
    mkdir -p models/base models/fine_tuned
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data
fi

# Check for GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✓ GPU detected:"
    nvidia-smi --query-gpu=name --format=csv,noheader
else
    echo "⚠️  No GPU detected. Will use CPU (slower inference)."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Train a model: python train.py --model gpt2 --quick-start"
echo "  2. Start server: python serve.py --model gpt2"
echo "  3. Test API: curl http://localhost:8001/"
echo ""
echo "For more info, see: QUICKSTART.md"
