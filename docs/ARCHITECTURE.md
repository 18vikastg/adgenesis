# ADGENESIS Architecture

Technical architecture and design decisions for the ADGENESIS platform.

## System Overview

ADGENESIS is a full-stack AI SaaS application that generates platform-compliant ad designs using OpenAI's GPT-4 API and renders them with Fabric.js.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│  PostgreSQL │
│  Frontend   │◀─────│   Backend    │◀─────│  (Supabase) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├─────────────┐
                            │             │
                     ┌──────▼────┐   ┌────▼────┐
                     │  OpenAI   │   │  AWS S3 │
                     │    API    │   │ Storage │
                     └───────────┘   └─────────┘
```

## Technology Stack

### Frontend
- **Framework:** React 18
- **Styling:** Tailwind CSS 3
- **Canvas:** Fabric.js 5
- **State Management:** React Query 3
- **HTTP Client:** Axios
- **File Upload:** React Dropzone
- **Routing:** React Router 6

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **ORM:** SQLAlchemy 2.0
- **Database Driver:** psycopg2
- **Validation:** Pydantic 2.0
- **AI:** OpenAI Python SDK
- **Image Processing:** Pillow
- **PDF Processing:** PyPDF2
- **Cloud Storage:** boto3 (AWS S3)

### Database
- **Type:** PostgreSQL 15+
- **Hosting:** Supabase (managed PostgreSQL)
- **Features Used:** JSONB, indexes, foreign keys, triggers

### Infrastructure
- **Frontend Hosting:** Vercel (planned)
- **Backend Hosting:** Railway (planned)
- **Database:** Supabase (free tier)
- **Storage:** AWS S3 (free tier)

## Architecture Patterns

### 1. Separation of Concerns

**Frontend Structure:**
```
frontend/src/
├── components/      # Reusable UI components
├── pages/          # Page-level components (routes)
├── services/       # API communication layer
└── utils/          # Helper functions
```

**Backend Structure:**
```
backend/app/
├── main.py         # FastAPI app initialization
├── models.py       # SQLAlchemy database models
├── schemas.py      # Pydantic request/response schemas
├── routes.py       # API endpoint definitions
└── utils.py        # Business logic & helpers
```

### 2. API-First Design

- RESTful API with clear resource naming
- JSON request/response format
- Automatic OpenAPI documentation
- Consistent error handling

### 3. Database Design

**Entity Relationship Diagram:**
```
┌─────────┐
│  users  │
└────┬────┘
     │
     ├─────────┬────────────┬──────────┐
     │         │            │          │
┌────▼────┐ ┌─▼─────────┐  │          │
│ designs │ │guidelines │  │          │
└────┬────┘ └───────────┘  │          │
     │                      │          │
     ├──────┬──────────┐    │          │
     │      │          │    │          │
┌────▼───┐ ┌▼─────────▼─┐  │          │
│exports │ │compliance_│  │          │
└────────┘ │   logs    │  │          │
           └───────────┘  │          │
```

**Key Design Decisions:**
- **JSONB for flexibility:** Canvas data and extracted guidelines stored as JSON
- **Foreign keys:** Maintain referential integrity
- **Indexes:** Optimize common queries (user_id, created_at)
- **Enums:** Platform and format types validated at DB level

## Core Flows

### 1. Design Generation Flow

```
User Input
    │
    ├─→ Frontend validates input
    │
    ├─→ API request to /api/designs/generate
    │
    ├─→ Backend constructs AI prompt
    │
    ├─→ OpenAI GPT-4 generates design spec
    │
    ├─→ Convert to Fabric.js JSON format
    │
    ├─→ Save to database
    │
    └─→ Return design to frontend
```

**AI Prompt Engineering:**
```python
system_prompt = f"""You are an expert ad designer.
Platform: {platform}
Format: {format} ({width}x{height})
User Request: {prompt}

Return JSON with:
- background_color (hex)
- elements (text, shapes, images)
- layout (composition rules)

Make it professional, eye-catching, and platform-compliant."""
```

### 2. Guideline Extraction Flow

```
User uploads PDF/Image
    │
    ├─→ Save file temporarily
    │
    ├─→ Extract text from PDF (PyPDF2)
    │
    ├─→ Send to OpenAI for structured extraction
    │
    ├─→ Parse JSON response (colors, fonts, logos)
    │
    ├─→ Save to database
    │
    ├─→ (Optional) Upload to S3 for permanent storage
    │
    └─→ Return extracted data
```

**Extraction Prompt:**
```python
"Extract brand guidelines from this text. Return JSON with:
- colors (hex codes)
- fonts (names)
- logo_description
- tone
- style_notes"
```

### 3. Compliance Check Flow

```
User requests compliance check
    │
    ├─→ Load design from database
    │
    ├─→ Get platform specifications
    │
    ├─→ Check dimensions
    │
    ├─→ Verify file size limits
    │
    ├─→ Check text ratio (for Meta)
    │
    ├─→ Analyze color contrast (future)
    │
    ├─→ Generate issues list
    │
    ├─→ Save to compliance_logs
    │
    └─→ Return compliance result
```

### 4. Export Flow

```
User selects design and format
    │
    ├─→ Load canvas JSON from database
    │
    ├─→ Render canvas to image (Pillow)
    │
    ├─→ Convert to requested format
    │
    ├─→ (Optional) Upload to S3
    │
    ├─→ Stream file to user
    │
    └─→ Log export in database
```

## Data Models

### Design Model
```python
{
  "id": 1,
  "user_id": 1,
  "prompt": "Summer sale ad...",
  "platform": "meta",
  "format": "square",
  "canvas_data": {
    "version": "5.3.0",
    "objects": [...],
    "background": "#ffffff",
    "width": 1080,
    "height": 1080
  },
  "is_compliant": 0,  # 0: not checked, 1: compliant, -1: non-compliant
  "created_at": "2025-11-30T12:00:00Z"
}
```

### Fabric.js Canvas Structure
```json
{
  "version": "5.3.0",
  "objects": [
    {
      "type": "textbox",
      "text": "SUMMER SALE",
      "left": 100,
      "top": 100,
      "fontSize": 48,
      "fill": "#ff6600",
      "fontFamily": "Arial"
    },
    {
      "type": "rect",
      "left": 0,
      "top": 0,
      "width": 1080,
      "height": 200,
      "fill": "#0066cc"
    }
  ],
  "background": "#ffffff",
  "width": 1080,
  "height": 1080
}
```

## Security Considerations

### Current (Hackathon)
- ❌ No authentication (demo user hardcoded)
- ❌ No authorization checks
- ❌ API keys in environment variables only
- ✅ CORS enabled for localhost
- ✅ Input validation with Pydantic
- ✅ SQL injection protected (SQLAlchemy ORM)

### Future Production
- Add JWT authentication
- Implement role-based access control
- Rate limiting per user
- File upload scanning
- API key rotation
- Request signing
- HTTPS enforcement

## Performance Optimization

### Current
- Database indexes on foreign keys
- React Query caching
- FastAPI async endpoints

### Future
- Redis caching for designs
- CDN for static assets
- Image optimization
- Lazy loading
- Database connection pooling
- Background job queue (Celery)

## Scalability

### Current Architecture
- Single server (Railway)
- Single database (Supabase)
- Handles ~100 concurrent users

### Scaling Strategy
1. **Horizontal scaling:** Multiple backend instances behind load balancer
2. **Database scaling:** Read replicas, connection pooling
3. **Caching layer:** Redis for sessions and frequent queries
4. **Async processing:** Celery for long-running tasks (AI generation, exports)
5. **CDN:** CloudFront for static assets and exports

## AI Integration

### OpenAI Usage

**Models:**
- GPT-4 for design generation
- GPT-4 for guideline extraction
- (Future) DALL-E 3 for image generation

**Cost Optimization:**
- Limit prompt size (4000 tokens max)
- Cache common responses
- Batch processing for multiple designs
- Use GPT-3.5-turbo for simple tasks

**Prompt Templates:**
```python
DESIGN_GENERATION_PROMPT = """
You are an expert ad designer. Generate a design for:
Platform: {platform}
Format: {format} ({width}x{height})
Brand colors: {colors}
Brand fonts: {fonts}
User request: {prompt}

Return JSON with elements, positions, colors, text.
"""

GUIDELINE_EXTRACTION_PROMPT = """
Extract brand guidelines from this document.
Return JSON with:
- colors (hex codes with names)
- fonts (font families)
- logos (descriptions)
- tone (brand voice)
- restrictions (what to avoid)
"""
```

## Error Handling

### Frontend
```javascript
try {
  const response = await api.generateDesign(data);
  // Success handling
} catch (error) {
  if (error.response) {
    // API error
    showError(error.response.data.detail);
  } else {
    // Network error
    showError('Network error. Please try again.');
  }
}
```

### Backend
```python
try:
    # Business logic
except OpenAIError as e:
    raise HTTPException(status_code=503, detail="AI service unavailable")
except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail="Database error")
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

## Testing Strategy

### Current (Hackathon)
- Manual testing
- API testing via Swagger UI

### Future
- **Frontend:** Jest + React Testing Library
- **Backend:** pytest + pytest-asyncio
- **Integration:** Postman collections
- **E2E:** Playwright
- **Load testing:** Locust

## Deployment

### Current Setup
```
Frontend (Vercel)
    │
    ├─→ Git push to main
    │
    ├─→ Automatic build
    │
    └─→ Deploy to vercel.app

Backend (Railway)
    │
    ├─→ Git push to main
    │
    ├─→ Docker build
    │
    └─→ Deploy to railway.app

Database (Supabase)
    │
    └─→ Always available (managed)
```

### Environment Variables
```
Frontend (.env)
├─→ REACT_APP_API_URL

Backend (.env)
├─→ OPENAI_API_KEY
├─→ DATABASE_URL
├─→ AWS_ACCESS_KEY_ID
├─→ AWS_SECRET_ACCESS_KEY
├─→ CORS_ORIGINS
```

## Monitoring & Logging

### Current
- Console logs
- Supabase dashboard for DB metrics

### Future
- Sentry for error tracking
- LogRocket for session replay
- DataDog for APM
- CloudWatch for infrastructure

## Compliance & Legal

### Platform Policies
- Meta Advertising Policies
- Google Ads Policies
- LinkedIn Advertising Guidelines

### Data Privacy
- Store minimal user data
- GDPR compliance (future)
- User data export (future)

## Future Enhancements

### Phase 1 (MVP+)
- User authentication (Auth0)
- Design templates library
- Collaborative editing
- Design versioning

### Phase 2 (Scale)
- Team workspaces
- A/B testing integration
- Analytics dashboard
- API rate limiting

### Phase 3 (Enterprise)
- White-label solution
- Custom model training
- Advanced compliance rules
- Multi-language support

## Technical Debt

### Known Issues
1. Export functionality is simplified (placeholder images)
2. No S3 upload implemented (files stored temporarily)
3. No background job processing
4. Limited error messages
5. No caching layer

### Prioritized Fixes
1. Implement actual canvas-to-image rendering
2. Add S3 integration for file storage
3. Improve error handling and messages
4. Add request validation
5. Implement rate limiting

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Fabric.js Documentation](http://fabricjs.com/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Supabase Documentation](https://supabase.com/docs)

---

**Architecture Version:** 1.0  
**Last Updated:** 2025-11-30  
**Maintained By:** ADGENESIS Team
