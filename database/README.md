# Database Setup Guide

This guide explains how to set up the PostgreSQL database for ADGENESIS using Supabase (free tier).

## Option 1: Supabase (Recommended for Hackathon)

### Step 1: Create Supabase Account
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up for a free account (no credit card required)
3. You get:
   - 500MB database storage
   - 2GB file storage
   - Unlimited API requests
   - Perfect for hackathons!

### Step 2: Create a New Project
1. Click "New Project"
2. Choose a name: `adgenesis`
3. Set a database password (save this!)
4. Select a region (closest to you)
5. Click "Create new project" (takes ~2 minutes)

### Step 3: Get Database URL
1. Go to Project Settings (gear icon)
2. Click "Database"
3. Scroll to "Connection string"
4. Copy the "URI" connection string
5. It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

### Step 4: Run Database Schema
1. In Supabase dashboard, click "SQL Editor" (left sidebar)
2. Click "New query"
3. Copy the entire contents of `database/schema.sql`
4. Paste into the query editor
5. Click "Run" button
6. You should see "Success. No rows returned"

### Step 5: Verify Tables
1. Click "Table Editor" (left sidebar)
2. You should see tables: `users`, `designs`, `guidelines`, `exports`, `compliance_logs`
3. Click on `users` table - you should see one row (demo-user-001)

### Step 6: Update Backend .env
1. Open `backend/.env`
2. Replace `DATABASE_URL` with your Supabase connection string:
   ```
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

## Option 2: Local PostgreSQL

If you prefer running PostgreSQL locally:

### Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**MacOS:**
```bash
brew install postgresql
brew services start postgresql
```

### Create Database
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE adgenesis;

# Create user (optional)
CREATE USER adgenesis_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE adgenesis TO adgenesis_user;

# Exit
\q
```

### Run Schema
```bash
psql -U postgres -d adgenesis -f database/schema.sql
```

### Update .env
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/adgenesis
```

## Testing Connection

Test the database connection:

```bash
cd backend
source venv/bin/activate
python -c "from app.utils import engine; print('Connected!' if engine.connect() else 'Failed')"
```

## Database Structure

### Tables

**users**
- Stores user accounts (simplified for hackathon)
- Demo user pre-created with ID: demo-user-001

**designs**
- Generated ad designs
- Contains AI-generated canvas data (Fabric.js JSON)
- Links to user and tracks compliance status

**guidelines**
- Uploaded brand guidelines
- Stores extracted data (colors, fonts, logos)

**exports**
- Exported design files
- Tracks format, file size, and download URLs

**compliance_logs**
- Platform compliance check results
- Stores issues found during validation

## Migrations

For future updates, run migration scripts in order:

```bash
psql -U postgres -d adgenesis -f database/migrations/001_initial_schema.sql
```

## Troubleshooting

### Connection Refused
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify port 5432 is open: `sudo netstat -plnt | grep 5432`

### Authentication Failed
- Double-check password in DATABASE_URL
- For Supabase, make sure you replaced `[YOUR-PASSWORD]` with actual password

### Tables Not Created
- Check for SQL syntax errors in Supabase SQL Editor
- Make sure you're connected to the right database

### Can't Connect from Backend
- Verify DATABASE_URL format is correct
- Test connection: `psql "postgresql://user:pass@host:5432/dbname"`

## Supabase Additional Features

Once set up, you can also use:

1. **Row Level Security (RLS)** - For production authentication
2. **Realtime Subscriptions** - For live updates
3. **Storage Buckets** - For storing design files
4. **Edge Functions** - For serverless functions

For this hackathon, we're using the basic database features only.

## Next Steps

After database setup:
1. Update `backend/.env` with your DATABASE_URL
2. Test the backend: `cd backend && uvicorn app.main:app --reload`
3. Visit `http://localhost:8000/docs` to see API documentation
4. The API should connect to the database automatically

---

**Need Help?**
- Supabase Docs: https://supabase.com/docs
- PostgreSQL Docs: https://www.postgresql.org/docs/
