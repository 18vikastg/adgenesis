# ADGENESIS - AI-Powered Design Platform

<div align="center">

**🎨 Create stunning designs with AI - From concept to export in seconds**

[![Made with React](https://img.shields.io/badge/React-18.2.0-blue?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-red?logo=pytorch)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 🚀 Overview

ADGENESIS is a **Canva-inspired AI-powered design platform** that empowers marketers, designers, and content creators to generate professional designs in seconds. Describe your vision, and watch AI create stunning ads, social media posts, posters, and more - all with an intuitive visual editor.

**🆓 100% FREE with custom ML model** - Generate unlimited designs without OpenAI costs!

## ✨ Features

### 🎯 **Core Design Tools**
- **AI-Powered Design Generation** - Text-to-design in seconds with custom ML model
- **Professional Canvas Editor** - Fabric.js-powered editor with layers, text, shapes, and images
- **Smart Template Library** - 50+ pre-built templates across categories (Social, Print, Marketing)
- **Brand Kit Management** - Store and manage brand colors, fonts, and logos
- **Multi-Format Export** - Export in PNG, JPG, SVG formats with custom dimensions
- **Real-time Preview** - Live canvas rendering with instant updates

### 🤖 **AI-Powered Features**
- **Custom Fine-Tuned ML Model** - GPT-2-based model trained on design data
- **Intelligent Theme Detection** - Auto-applies professional color schemes (Tech, Fashion, Business, Food, Sale)
- **Design Blueprint Generation** - AI creates complete design layouts with typography, colors, and composition
- **Image Analysis & Conversion** - Upload images and convert them to editable designs
- **Smart Prompts** - Natural language understanding for design generation

### 🎨 **Design Studio**
- **Drag-and-Drop Editor** - Intuitive interface for element manipulation
- **Layer Management** - Organize and control design elements
- **Text Styling** - Rich text formatting with custom fonts and effects
- **Shape Tools** - Rectangles, circles, and custom shapes
- **Image Upload** - Add and manipulate images within designs
- **Color Picker** - Advanced color selection with brand colors
- **Undo/Redo** - Full history tracking
- **Keyboard Shortcuts** - Professional workflow shortcuts

### 📱 **Platform & Templates**
- **Social Media** - Instagram Posts/Stories, Facebook, Twitter, LinkedIn formats
- **Print Design** - Posters, flyers, business cards
- **Marketing** - Ad banners, promotional graphics
- **Custom Sizes** - Support for any dimension

### 🎯 **Professional Features**
- **Multi-Platform Compliance** - Auto-check specs for Meta, Google Ads, LinkedIn
- **Brand Guidelines Parser** - Upload PDFs to extract brand assets
- **Project Management** - Save, organize, and retrieve designs
- **Responsive Dashboard** - Modern UI with dark/light mode support
- **Template Categories** - Filter by industry, platform, and use case


## 🛠️ Tech Stack

### **Frontend**
- **React 18.2.0** - Modern UI framework with hooks
- **React Router DOM 6.20** - Client-side routing and navigation
- **Tailwind CSS 3.3.6** - Utility-first CSS framework
- **Fabric.js 5.3.0** - Canvas manipulation and rendering engine
- **React Query 3.39** - Server state management and caching
- **Axios 1.6.2** - HTTP client for API communication
- **React Dropzone** - File upload functionality

### **Backend**
- **FastAPI 0.104** - High-performance Python web framework
- **Uvicorn** - Lightning-fast ASGI server
- **SQLAlchemy 2.0.23** - SQL ORM for database operations
- **Pydantic 2.5.2** - Data validation and settings management
- **OpenAI API 1.54.0** - AI integration (optional fallback)
- **Pillow 10.1.0** - Image processing and export
- **Boto3** - AWS S3 integration for storage
- **psycopg2** - PostgreSQL database adapter
- **Python-multipart** - File upload handling

### **ML Pipeline**
- **PyTorch 2.1.0+** - Deep learning framework
- **Transformers 4.36.0+** - Hugging Face model hub
- **Accelerate** - Distributed training and optimization
- **PEFT (LoRA)** - Parameter-efficient fine-tuning
- **bitsandbytes** - Model quantization for efficiency
- **Datasets** - Dataset loading and processing
- **Scikit-learn** - ML utilities and evaluation
- **WandB** (optional) - Experiment tracking

### **Database & Storage**
- **PostgreSQL** - Primary relational database (via Supabase)
- **Supabase** - Backend-as-a-Service platform
- **In-memory storage** - Fast development mode without DB

### **DevOps & Infrastructure**
- **Docker** - Containerization
- **Git** - Version control
- **Python dotenv** - Environment configuration
- **Node.js 18+** - JavaScript runtime
- **npm** - Package management


## 📁 Project Structure

```
adgenesis/
├── frontend/                    # React Application
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── AdvancedEditor.jsx
│   │   │   ├── Editor.jsx
│   │   │   ├── Navbar.js
│   │   │   ├── TemplateGallery.jsx
│   │   │   └── ui/              # UI primitives
│   │   ├── pages/               # Page components
│   │   │   ├── LandingPage.jsx  # Landing page (/)
│   │   │   ├── Dashboard.jsx    # Main dashboard
│   │   │   ├── Editor.jsx       # Design editor
│   │   │   ├── Templates.jsx    # Template gallery
│   │   │   ├── Projects.jsx     # Project management
│   │   │   ├── BrandKit.jsx     # Brand assets
│   │   │   ├── AnalyzePage.jsx  # Image analysis
│   │   │   └── AboutPage.jsx    # About page
│   │   ├── layouts/
│   │   │   └── DashboardLayout.jsx
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── data/
│   │   │   └── templates.js     # Template definitions
│   │   ├── styles/
│   │   │   └── design-system.css
│   │   ├── App.js               # Main app component
│   │   └── index.js             # Entry point
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                     # FastAPI Application
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── routes.py            # API endpoints
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── utils.py             # Helper functions
│   │   └── model_adapter.py     # ML/OpenAI switching
│   ├── requirements.txt
│   ├── start.sh
│   └── venv/                    # Python virtual environment
│
├── ml_pipeline/                 # Machine Learning Service
│   ├── serve.py                 # Inference server (port 8001)
│   ├── train.py                 # Model training script
│   ├── config.py                # ML configuration
│   ├── creative_director.py     # Design intelligence
│   ├── design_analyzer.py       # Design analysis
│   ├── design_schema.py         # Design data structures
│   ├── image_generator.py       # Image generation
│   ├── modern_design_system.py  # Design systems
│   ├── smart_design_generator.py
│   ├── premium_design_generator.py
│   ├── professional_design_generator.py
│   ├── data/
│   │   ├── training_data.json
│   │   └── design_training_data.json
│   ├── models/
│   │   ├── base/                # Base models
│   │   └── fine_tuned/          # Trained models (548MB)
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── generated_designs/       # Output designs
│   └── requirements.txt
│
├── database/                    # Database Schema
│   ├── schema.sql               # PostgreSQL schema
│   ├── migrations/
│   │   └── 001_initial_schema.sql
│   └── README.md
│
├── docs/                        # Documentation
│   ├── LOCAL_SETUP.md           # Setup guide
│   ├── API.md                   # API documentation
│   ├── ARCHITECTURE.md          # Architecture overview
│   └── EDITOR.md                # Editor features
│
├── generated_designs/           # Generated design outputs
├── generated_images/            # Generated image outputs
├── .gitignore
├── .env.example                 # Environment template
└── README.md                    # This file
```


## 🚦 Quick Start

### **Prerequisites**
- **Python 3.10+** with pip
- **Node.js 18+** and npm
- **Git** for cloning the repository
- (Optional) Hugging Face API key for AI image generation

### **One-Command Setup & Run**

```bash
# Clone the repository
git clone https://github.com/18vikastg/adgenesis.git
cd adgenesis

# Install dependencies (first time only)
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
cd ml_pipeline && pip install -r requirements.txt && cd ..
```

### **Start All Services**

**Terminal 1 - ML Service (Port 8001):**
```bash
cd ml_pipeline
python serve.py --model gpt2
```

**Terminal 2 - Backend API (Port 8000):**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 - Frontend (Port 3000):**
```bash
cd frontend
npm start
```

🎉 **Open http://localhost:3000** in your browser!

### **Quick Test**

1. **Landing Page** - Opens at `http://localhost:3000/`
2. **Dashboard** - Navigate to `/dashboard`
3. **Create Design**:
   - Click "Start Designing" or go to Dashboard
   - Enter a prompt: `"Create a tech startup ad with blue theme"`
   - Click "Generate Design"
   - Edit in the canvas editor
   - Export as PNG/JPG/SVG

### **Available Routes**

| Route | Description |
|-------|-------------|
| `/` | Landing page with features showcase |
| `/dashboard` | Main dashboard with quick actions |
| `/dashboard/templates` | Template gallery (50+ templates) |
| `/dashboard/projects` | Your saved projects |
| `/dashboard/brand-kit` | Brand colors, fonts, and logos |
| `/dashboard/analyze` | Image analysis and conversion |
| `/editor` | Full-featured design editor |
| `/about` | About the platform |


## 🎨 Using the Application

### **1. Landing Page**
- Modern, Canva-inspired design
- Feature showcase with animations
- Quick access to dashboard and templates

### **2. Dashboard**
- **Recent Designs** - View your latest creations
- **Quick Actions** - Start new designs by size preset
- **Templates** - Browse categorized templates
- **Stats** - Design analytics and usage

### **3. AI Design Generation**
Enter natural language prompts like:
- `"Create a modern tech startup ad with blue theme"`
- `"Design a fashion sale poster with vibrant colors"`
- `"Make a professional business presentation"`
- `"Create a food delivery ad with orange and green"`
- `"Generate a minimalist Instagram post"`

**Supported Themes:**
- **Tech** - Dark blue (#1a1a2e) with bright accents
- **Fashion** - Pink (#ff6b9d) with yellow highlights
- **Sale** - Red (#dc2626) with urgency colors
- **Business** - Navy (#1e3a8a) with gold accents
- **Food** - Orange (#f97316) with fresh green
- **Default** - Purple gradient for general use

### **4. Design Editor**
- **Canvas Tools**:
  - Add/edit text with rich formatting
  - Insert shapes (rectangles, circles)
  - Upload and manipulate images
  - Layer management and ordering
  - Color picker with brand colors
- **Controls**:
  - Zoom in/out
  - Undo/redo (Ctrl+Z / Ctrl+Y)
  - Align elements
  - Duplicate objects
  - Delete elements
- **Export**:
  - PNG (high quality)
  - JPG (optimized)
  - SVG (vector)
  - Custom dimensions

### **5. Template Gallery**
- **50+ Professional Templates**
- **Categories**: Social Media, Marketing, Print, Business
- **Platforms**: Instagram, Facebook, Twitter, LinkedIn, YouTube
- **Filters**: Search, category, platform
- **One-click use** - Customize in editor

### **6. Brand Kit**
- **Colors**: Save brand color palettes
- **Fonts**: Manage typography
- **Logos**: Upload and organize brand assets
- **Quick Apply**: Use brand elements in designs

### **7. Image Analysis**
- Upload existing designs
- AI analyzes and converts to editable format
- Extract colors, text, and layout
- Edit and enhance converted designs

### **8. Project Management**
- Save designs with automatic versioning
- Organize in folders
- Search and filter
- Share and export


## 🔑 Environment Variables

Create `.env` files in the respective directories:

### **Backend (.env)**
```env
# API Configuration
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# OpenAI (Optional - for fallback)
OPENAI_API_KEY=your_openai_key_here

# ML Service
ML_SERVICE_URL=http://localhost:8001

# Database (Optional - Supabase)
DATABASE_URL=postgresql://user:password@host:port/dbname
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# AWS S3 (Optional - for production storage)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=your_bucket_name
```

### **Frontend (.env)**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ML_URL=http://localhost:8001
```

### **ML Pipeline (.env)**
```env
# Hugging Face (Optional - for image generation)
HUGGINGFACE_API_KEY=your_hf_token_here

# Model Configuration
MODEL_NAME=gpt2
MODEL_PATH=./models/fine_tuned/gpt2
```

## 📊 API Endpoints

### **Design Generation**
- `POST /api/designs/generate` - Generate new design from prompt
- `GET /api/designs` - List all designs
- `GET /api/designs/{id}` - Get specific design
- `PUT /api/designs/{id}` - Update design
- `GET /api/designs/{id}/export` - Export design

### **Guidelines & Brand Kit**
- `POST /api/guidelines/upload` - Upload brand guidelines PDF
- `GET /api/guidelines` - List brand guidelines
- `GET /api/guidelines/{id}` - Get specific guideline

### **Compliance**
- `POST /api/compliance/check` - Check platform compliance

### **ML Service**
- `POST /generate` - Generate design blueprint
- `GET /health` - Health check
- `GET /model/info` - Model information

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend   │─────▶│ ML Pipeline │
│  React SPA  │      │   FastAPI   │      │  PyTorch    │
│  Port 3000  │      │  Port 8000  │      │  Port 8001  │
└─────────────┘      └─────────────┘      └─────────────┘
       │                    │                     │
       │                    │                     │
       ▼                    ▼                     ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Browser   │      │  PostgreSQL │      │   Models    │
│   Storage   │      │  (Supabase) │      │  Fine-tuned │
└─────────────┘      └─────────────┘      └─────────────┘
```

### **Key Components**

1. **Frontend (React)**
   - User interface and design editor
   - Canvas rendering with Fabric.js
   - State management with React Query
   - API communication via Axios

2. **Backend (FastAPI)**
   - RESTful API endpoints
   - Design generation orchestration
   - Database operations
   - File upload/export handling
   - Model adapter for ML/OpenAI switching

3. **ML Pipeline (PyTorch)**
   - Custom fine-tuned GPT-2 model
   - Design blueprint generation
   - Theme detection and color schemes
   - Inference server with FastAPI

4. **Database (PostgreSQL)**
   - User management
   - Design storage
   - Brand guidelines
   - Export history

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# ML model tests
cd ml_pipeline
python test_service.py
python test_blueprint_generation.py
```

## 📚 Documentation

- **[LOCAL_SETUP.md](docs/LOCAL_SETUP.md)** - Detailed setup instructions
- **[API.md](docs/API.md)** - Complete API documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
- **[EDITOR.md](docs/EDITOR.md)** - Editor features and shortcuts

## 🎯 Use Cases

- **Marketing Teams** - Create ad campaigns quickly
- **Social Media Managers** - Generate platform-specific content
- **Small Businesses** - Professional designs without designers
- **Content Creators** - Consistent brand visuals
- **Agencies** - Scale design production
- **Startups** - MVP and marketing materials

## 🚀 Deployment

### **Frontend (Vercel/Netlify)**
```bash
cd frontend
npm run build
# Deploy build/ folder
```

### **Backend (Railway/Render)**
```bash
# Use Docker or direct Python deployment
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **ML Service (Hugging Face Spaces/Modal)**
```bash
cd ml_pipeline
python serve.py --model gpt2 --host 0.0.0.0 --port 8001
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Vikas TG** - [@18vikastg](https://github.com/18vikastg)

## 🙏 Acknowledgments

- Hugging Face for Transformers library
- OpenAI for GPT models
- Fabric.js for canvas rendering
- FastAPI for the amazing web framework
- React team for the frontend framework
- Tailwind CSS for styling utilities

## 📧 Contact

For questions, issues, or suggestions:
- GitHub Issues: [Create an issue](https://github.com/18vikastg/adgenesis/issues)
- Email: [Contact](mailto:your-email@example.com)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Built by Vikas TG

</div>

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
