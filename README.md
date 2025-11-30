# ADGENESIS - AI-Powered Ad Design Platform

**Automate compliant ad creation with AI-powered design generation and brand guideline enforcement.**

## 🚀 Overview

ADGENESIS is an AI SaaS platform that helps marketers and designers create platform-compliant advertisements in seconds. Upload your brand guidelines, describe your ad concept, and let AI generate professional designs that meet platform requirements (Meta, Google, LinkedIn).

## ✨ Key Features

- **AI Design Generation**: Generate ad designs from text prompts using OpenAI + Fabric.js
- **Brand Guideline Parser**: Upload brand PDFs, AI extracts colors, fonts, logos
- **Multi-Platform Compliance**: Auto-check ad specs for Meta, Google Ads, LinkedIn
- **Real-time Preview**: Interactive canvas editor with live modifications
- **Batch Export**: Export designs in multiple formats (PNG, JPG, SVG, PDF)
- **Template Library**: Pre-built templates for different ad types

## 🛠️ Tech Stack

### Frontend
- React 18 with Create React App
- Tailwind CSS for styling
- Fabric.js for canvas manipulation
- React Query for data fetching
- Axios for API calls

### Backend
- FastAPI (Python 3.10+)
- OpenAI API for AI generation
- Pillow for image processing
- PostgreSQL (Supabase) for data storage
- AWS S3 for file storage

### Infrastructure
- Frontend: Vercel (free tier)
- Backend: Railway (free tier)
- Database: Supabase (free tier)
- Storage: AWS S3 (free tier)

## 📁 Project Structure

```
adgenesis/
├── frontend/               # React application
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   ├── utils/         # Helper functions
│   │   └── App.js
│   ├── package.json
│   └── .env.example
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── main.py       # FastAPI app entry
│   │   ├── models.py     # Database models
│   │   ├── routes.py     # API endpoints
│   │   ├── utils.py      # Helper functions
│   │   └── schemas.py    # Pydantic schemas
│   ├── requirements.txt
│   └── .env.example
├── database/              # Database setup
│   ├── schema.sql        # PostgreSQL schema
│   └── migrations/       # SQL migrations
├── docs/                  # Documentation
│   ├── LOCAL_SETUP.md
│   ├── API.md
│   └── ARCHITECTURE.md
├── .gitignore
└── setup-dev.sh          # Development setup script
```

## 🚦 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL (or Supabase account)
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/18vikastg/adgenesis.git
cd adgenesis

# Run automated setup
chmod +x setup-dev.sh
./setup-dev.sh

# Or manually follow docs/LOCAL_SETUP.md
```

### Running Locally

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm start
```

Access the app at `http://localhost:3000`

## 🔑 Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/adgenesis
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=adgenesis-assets
CORS_ORIGINS=http://localhost:3000
```

## 📖 Documentation

- [Local Setup Guide](docs/LOCAL_SETUP.md) - Step-by-step development setup
- [API Documentation](docs/API.md) - Complete API endpoint reference
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and technical decisions

## 🎯 Roadmap

- [ ] User authentication (Auth0)
- [ ] Team collaboration features
- [ ] Advanced AI prompt engineering
- [ ] A/B testing integration
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📝 License

MIT License - See LICENSE file for details

## 🙋 Support

For questions or issues, please open a GitHub issue.

---

**Built By Vikas T G**
