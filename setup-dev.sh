#!/bin/bash

# ADGENESIS Development Setup Script
# This script automates the complete local development environment setup

set -e  # Exit on any error

echo "🚀 ADGENESIS Development Setup"
echo "================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node --version) found${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed. Please install Python 3.10+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version) found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed. Please install npm${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm $(npm --version) found${NC}"

echo ""
echo "📦 Setting up Backend..."
echo "------------------------"

# Setup Backend
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ Created .env file. Please update with your API keys!${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
fi

deactivate
cd ..

echo ""
echo "🎨 Setting up Frontend..."
echo "-------------------------"

# Setup Frontend
cd frontend

# Install dependencies
echo "Installing Node dependencies (this may take a few minutes)..."
npm install
echo -e "${GREEN}✓ Node dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
fi

cd ..

echo ""
echo "🗄️  Database Setup"
echo "------------------"
echo -e "${YELLOW}To complete setup:${NC}"
echo "1. Create a Supabase account at https://supabase.com"
echo "2. Create a new project"
echo "3. Run the SQL in database/schema.sql in Supabase SQL editor"
echo "4. Update DATABASE_URL in backend/.env"
echo ""

echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo ""
echo "1. Update environment variables:"
echo "   - backend/.env (OPENAI_API_KEY, DATABASE_URL, AWS credentials)"
echo "   - frontend/.env (REACT_APP_API_URL if not using default)"
echo ""
echo "2. Start the development servers:"
echo ""
echo "   Terminal 1 (Backend):"
echo "   $ cd backend"
echo "   $ source venv/bin/activate"
echo "   $ uvicorn app.main:app --reload --port 8000"
echo ""
echo "   Terminal 2 (Frontend):"
echo "   $ cd frontend"
echo "   $ npm start"
echo ""
echo "3. Access the app at http://localhost:3000"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
