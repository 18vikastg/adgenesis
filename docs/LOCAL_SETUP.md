# Local Development Setup Guide

Complete step-by-step guide to set up ADGENESIS on your local machine.

## Prerequisites

Before you begin, ensure you have:

- **Node.js 18+** and npm ([Download](https://nodejs.org/))
- **Python 3.10+** ([Download](https://www.python.org/))
- **Git** ([Download](https://git-scm.com/))
- **PostgreSQL** OR a [Supabase](https://supabase.com) account (free)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

## Quick Setup (Automated)

If you want to skip manual steps, use the automated setup script:

```bash
chmod +x setup-dev.sh
./setup-dev.sh
```

Then skip to **Step 5: Configure Environment Variables**.

## Manual Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/adgenesis.git
cd adgenesis
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Go back to root
cd ..
```

**Verify backend installation:**
```bash
cd backend
source venv/bin/activate
python -c "import fastapi; import openai; print('✓ Backend dependencies installed')"
cd ..
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (this takes 2-3 minutes)
npm install

# Go back to root
cd ..
```

**Verify frontend installation:**
```bash
cd frontend
npm list react react-dom
cd ..
```

### Step 4: Database Setup

Choose **Option A (Supabase - Recommended)** OR **Option B (Local PostgreSQL)**:

#### Option A: Supabase (Recommended)

1. Create account at [https://supabase.com](https://supabase.com)
2. Create new project: `adgenesis`
3. Copy your connection string from Project Settings → Database
4. Go to SQL Editor and run the SQL from `database/schema.sql`
5. Verify tables are created in Table Editor

**Detailed instructions:** See `database/README.md`

#### Option B: Local PostgreSQL

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database
sudo -u postgres psql -c "CREATE DATABASE adgenesis;"

# Run schema
sudo -u postgres psql -d adgenesis -f database/schema.sql
```

### Step 5: Configure Environment Variables

#### Backend Configuration

```bash
# Copy example file
cp backend/.env.example backend/.env

# Edit backend/.env
nano backend/.env  # or use any text editor
```

Update these values in `backend/.env`:

```bash
# REQUIRED: OpenAI API Key
OPENAI_API_KEY=sk-proj-your_actual_openai_api_key_here

# REQUIRED: Database URL (from Supabase or local)
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

# OPTIONAL: AWS S3 (can skip for now)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=adgenesis-assets
AWS_REGION=us-east-1

# Default CORS (keep as is)
CORS_ORIGINS=http://localhost:3000
```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Supabase URL: Project Settings → Database → Connection String
- AWS (optional): https://console.aws.amazon.com/iam/

#### Frontend Configuration

```bash
# Copy example file
cp frontend/.env.example frontend/.env

# Edit frontend/.env (usually no changes needed)
nano frontend/.env
```

Default content (should work as-is):
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Step 6: Verify Setup

```bash
# Test backend
cd backend
source venv/bin/activate
python -c "from app.utils import get_db; print('✓ Backend configured correctly')"
cd ..

# Test frontend
cd frontend
npm run build --dry-run 2>&1 | grep -q "Creating an optimized" && echo "✓ Frontend configured correctly"
cd ..
```

## Running the Application

### Start Backend Server

```bash
# Terminal 1
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify backend:** Visit http://localhost:8000/docs (FastAPI auto-generated docs)

### Start Frontend Development Server

```bash
# Terminal 2 (open a new terminal)
cd frontend
npm start
```

You should see:
```
Compiled successfully!

You can now view adgenesis-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Verify frontend:** Visit http://localhost:3000

## Testing the Application

### 1. Upload Brand Guidelines

1. Go to http://localhost:3000/guidelines
2. Click or drag a PDF file
3. Wait for extraction (uses OpenAI)
4. See extracted colors and fonts

### 2. Generate a Design

1. Go to http://localhost:3000/studio
2. Enter prompt: "Summer sale ad with beach theme, 50% off text"
3. Select platform: Meta
4. Select format: Square
5. Click "Generate Design"
6. Wait for AI generation (~5-10 seconds)

### 3. Export Design

1. Go to http://localhost:3000/export
2. Select generated designs
3. Choose format (PNG, JPG, SVG, PDF)
4. Click "Export Selected"

## Common Issues & Solutions

### Backend Won't Start

**Error: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
cd backend
source venv/bin/activate  # Make sure venv is activated!
pip install -r requirements.txt
```

**Error: `Could not connect to database`**
- Check DATABASE_URL in `backend/.env`
- Test connection: `psql "your_database_url_here"`
- Verify Supabase project is active

**Error: `OpenAI API key not found`**
- Check OPENAI_API_KEY in `backend/.env`
- Get key from https://platform.openai.com/api-keys
- Make sure there are no extra spaces

### Frontend Won't Start

**Error: `npm: command not found`**
```bash
# Install Node.js from https://nodejs.org/
# Then verify:
node --version
npm --version
```

**Error: `Failed to compile`**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

**Error: `Port 3000 is already in use`**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
# Or use a different port
PORT=3001 npm start
```

### Database Issues

**Error: `relation "users" does not exist`**
```bash
# Schema not applied. Run:
# For Supabase: Run database/schema.sql in SQL Editor
# For local: psql -d adgenesis -f database/schema.sql
```

**Error: `permission denied for table users`**
- Check database user has proper permissions
- For Supabase, use the connection string from dashboard

### API Connection Issues

**Error: `Network Error` in browser console**
- Check backend is running on port 8000
- Verify REACT_APP_API_URL in `frontend/.env`
- Check CORS_ORIGINS in `backend/.env` includes frontend URL

## Development Workflow

### Making Changes

**Backend changes:**
- Edit files in `backend/app/`
- Server auto-reloads (thanks to `--reload` flag)
- Check http://localhost:8000/docs for API changes

**Frontend changes:**
- Edit files in `frontend/src/`
- Browser auto-refreshes
- Check browser console for errors

**Database changes:**
- Create new migration in `database/migrations/`
- Apply with: `psql -d adgenesis -f database/migrations/00X_name.sql`

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "Add feature description"

# Push to GitHub
git push origin feature/my-feature
```

## Deployment (Quick Notes)

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway)
```bash
cd backend
railway up
```

### Database (Supabase)
- Already hosted! Just update connection string

**Detailed deployment guide:** Coming soon

## Next Steps

1. **Read API Documentation:** `docs/API.md`
2. **Understand Architecture:** `docs/ARCHITECTURE.md`
3. **Start Building Features:** Check GitHub issues
4. **Join Community:** Link to Discord/Slack

## Getting Help

- **Documentation Issues:** Open GitHub issue
- **Bug Reports:** Use GitHub issue template
- **Questions:** Check FAQ or ask in community

---

**Setup Time Estimate:**
- Automated: ~10 minutes
- Manual: ~20 minutes
- First-time: ~30 minutes (including account creation)

**You're all set! Happy coding! 🚀**
