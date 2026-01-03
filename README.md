# ADGENESIS - AI-Powered Ad Design Platform

**Automate compliant ad creation with AI-powered design generation - 100% FREE with custom ML model!**

## 🚀 Overview

ADGENESIS is an AI SaaS platform that helps marketers and designers create platform-compliant advertisements in seconds. Upload your brand guidelines, describe your ad concept, and let AI generate professional designs that meet platform requirements (Meta, Google, LinkedIn).

**NEW**: Now powered by a custom fine-tuned ML model - **generate unlimited ads for FREE** with zero OpenAI costs!

## ✨ Key Features

- **Custom ML Model**: Fine-tuned GPT-2 model with intelligent fallback system
- **Zero Cost Generation**: Generate unlimited ads without OpenAI API costs
- **Professional Templates**: 6 built-in themes (Tech, Fashion, Sale, Business, Food, Default)
- **AI Design Generation**: Generate ad designs from text prompts in seconds
- **Brand Guideline Parser**: Upload brand PDFs, AI extracts colors, fonts, logos
- **Multi-Platform Compliance**: Auto-check ad specs for Meta, Google Ads, LinkedIn
- **Real-time Preview**: Interactive canvas editor with live modifications (800x800 display)
- **Batch Export**: Export designs in multiple formats (PNG, JPG, SVG)
- **Template Library**: Pre-built templates for different ad types

## 🛠️ Tech Stack

### Frontend
- React 18 with Create React App
- Tailwind CSS for styling
- Fabric.js for canvas manipulation and rendering
- React Query for data fetching
- Axios for API calls

### Backend
- FastAPI (Python 3.10+)
- Custom ML Model (GPT-2 fine-tuned) OR OpenAI API (switchable)
- Pillow (PIL) for image export and processing
- PostgreSQL (Supabase) for data storage
- Model Adapter pattern for provider switching

### ML Pipeline
- Transformers (Hugging Face) for model training
- PyTorch for deep learning
- PEFT/LoRA for efficient fine-tuning
- FastAPI for inference server
- Accelerate for distributed training

### Infrastructure
- Frontend: Localhost:3000 (React Dev Server)
- Backend: Localhost:8000 (FastAPI)
- ML Service: Localhost:8001 (Inference Server)
- Database: Supabase (free tier)

## 📁 Project Structure

```
adgenesis/
├── frontend/               # React application
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components (DesignStudioPage.js)
│   │   ├── services/      # API service layer
│   │   ├── utils/         # Helper functions
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── main.py       # Application entry
│   │   ├── routes.py     # API routes
│   │   ├── utils.py      # Design generation & export
│   │   ├── model_adapter.py  # ML/OpenAI switching
│   ├── venv/             # Python virtual environment
├── ml_pipeline/          # Custom ML model
│   ├── train.py          # Model training script
│   ├── serve.py          # Inference server (port 8001)
│   ├── config.py         # ML configuration
│   ├── data/
│   │   └── training_data.json  # Training examples
│   ├── models/
│   │   └── fine_tuned/   # Trained model weights (548MB)
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

## 🚦 Quick Start (EASIEST METHOD!)

### One-Command Startup

```bash
# Clone the repository
git clone https://github.com/18vikastg/adgenesis.git
cd adgenesis

# OPTIONAL: Set up Hugging Face API key for AI image generation
./setup_env.sh  # Follow instructions to add your HF token

# Run the complete startup script (starts all 3 services)
./run_all.sh
```

The script will automatically:
- ✅ Start ML Service on port 8001
- ✅ Start Backend on port 8000  
- ✅ Start Frontend on port 3000
- ✅ Open browser at http://localhost:3000

**Press Ctrl+C to stop all services**

> **💡 Note**: AI image generation requires a free Hugging Face API key.  
> See [docs/HUGGINGFACE_SETUP.md](docs/HUGGINGFACE_SETUP.md) for detailed setup instructions.

### Manual Startup (Alternative)

If you prefer to run services individually in separate terminals:

**Terminal 1 - ML Service:**
```bash
cd adgenesis
source backend/venv/bin/activate
cd ml_pipeline
python serve.py --model gpt2
```

**Terminal 2 - Backend:**
```bash
cd adgenesis/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 - Frontend:**
```bash
cd adgenesis/frontend
npm start
```

### Prerequisites
- Python 3.10+ with pip
- Node.js 18+ and npm
- Virtual environment already included in repo
- **Optional**: [Hugging Face API key](docs/HUGGINGFACE_SETUP.md) for AI image generation

### First Time Setup

```bash
# Install Python dependencies (if not already done)
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# The ML model is already trained (548MB in ml_pipeline/models/fine_tuned/gpt2)
```

## 🎨 Using the Application

1. **Open** http://localhost:3000 in your browser
2. **Navigate** to "Design Studio" tab
3. **Enter a prompt** like:
   - "Create a tech startup ad"
   - "Create a fashion sale ad"
   - "Create a food delivery ad"
   - "Create a business presentation"
4. **Click** "Generate Design"
5. **View** your design rendered on the canvas (800x800px)
6. **Edit** elements by clicking the "Edit" button
7. **Export** as PNG by clicking the "Export" button

### Available Themes

The ML model automatically detects keywords and applies professional color schemes:

- **Tech**: Dark blue background (#1a1a2e) with bright blue accents
- **Fashion**: Pink background (#ff6b9d) with yellow accents
- **Sale**: Red background (#dc2626) with yellow/orange accents
- **Business**: Navy background (#1e3a8a) with gold accents
- **Food**: Orange background (#f97316) with green accents
- **Default**: Purple gradient for general use

## 🔑 Environment Variables

### Backend (.env)
```bash
# Model Configuration
MODEL_PROVIDER=custom        # Use "custom" for ML model, "openai" for OpenAI API
ML_SERVICE_URL=http://localhost:8001

# Optional: Only needed if using OpenAI
OPENAI_API_KEY=your_key_here

# Database (optional for now)
DATABASE_URL=postgresql://user:pass@localhost:5432/adgenesis
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill services on specific ports
lsof -ti:8001 | xargs kill -9  # ML Service
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

### Check Service Logs
```bash
tail -f /tmp/ml_service.log   # ML Service logs
tail -f /tmp/backend.log      # Backend logs
tail -f /tmp/frontend.log     # Frontend logs
```

### Canvas Showing Blank White Screen
- **Fixed!** Latest version includes manual object rendering
- Canvas now properly scales 1080x1080 designs to 800x800 display
- Background colors render correctly

### Export Showing Blank Image
- **Fixed!** Export now uses PIL to render actual canvas data
- Text, rectangles, and colors are properly drawn
- Exports work for PNG, JPG, and SVG formats

## 📖 Documentation

- [Local Setup Guide](docs/LOCAL_SETUP.md) - Detailed development setup
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
