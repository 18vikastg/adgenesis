# API Documentation

Complete reference for ADGENESIS REST API.

**Base URL:** `http://localhost:8000/api` (development)

**Authentication:** None (demo user hardcoded for hackathon)

**Content-Type:** `application/json`

## Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/designs/generate` | POST | Generate new design with AI |
| `/designs` | GET | List all designs |
| `/designs/{id}` | GET | Get specific design |
| `/designs/{id}/export` | GET | Export design file |
| `/guidelines/upload` | POST | Upload brand guidelines |
| `/guidelines` | GET | List all guidelines |
| `/guidelines/{id}` | GET | Get specific guideline |
| `/compliance/check` | POST | Check design compliance |

---

## Designs

### Generate Design

Create a new ad design using AI based on text prompt.

**Endpoint:** `POST /api/designs/generate`

**Request Body:**
```json
{
  "prompt": "Summer sale ad with beach theme, 50% off text, vibrant colors",
  "platform": "meta",
  "format": "square",
  "guideline_id": 1
}
```

**Parameters:**
- `prompt` (string, required): Description of desired ad design (1-1000 chars)
- `platform` (string, required): Target platform - `meta`, `google`, or `linkedin`
- `format` (string, required): Ad format - `square`, `landscape`, `portrait`, or `story`
- `guideline_id` (integer, optional): ID of brand guideline to apply

**Response:** `201 Created`
```json
{
  "id": 1,
  "prompt": "Summer sale ad with beach theme, 50% off text, vibrant colors",
  "platform": "meta",
  "format": "square",
  "canvas_data": {
    "version": "5.3.0",
    "objects": [...],
    "background": "#ffffff",
    "width": 1080,
    "height": 1080
  },
  "preview_url": null,
  "is_compliant": 0,
  "created_at": "2025-11-30T12:00:00Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/designs/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Black Friday sale, bold red text, urgent",
    "platform": "meta",
    "format": "square"
  }'
```

---

### List Designs

Get all designs for the current user.

**Endpoint:** `GET /api/designs`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "prompt": "Summer sale ad...",
    "platform": "meta",
    "format": "square",
    "canvas_data": {...},
    "preview_url": null,
    "is_compliant": 0,
    "created_at": "2025-11-30T12:00:00Z"
  },
  {
    "id": 2,
    "prompt": "Holiday special...",
    "platform": "google",
    "format": "landscape",
    "canvas_data": {...},
    "preview_url": null,
    "is_compliant": 1,
    "created_at": "2025-11-30T11:00:00Z"
  }
]
```

**Example:**
```bash
curl http://localhost:8000/api/designs
```

---

### Get Design

Get a specific design by ID.

**Endpoint:** `GET /api/designs/{id}`

**Path Parameters:**
- `id` (integer): Design ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "prompt": "Summer sale ad with beach theme",
  "platform": "meta",
  "format": "square",
  "canvas_data": {
    "version": "5.3.0",
    "objects": [
      {
        "type": "textbox",
        "text": "SUMMER SALE",
        "left": 100,
        "top": 100,
        "fontSize": 48,
        "fill": "#ff6600"
      }
    ],
    "background": "#ffffff",
    "width": 1080,
    "height": 1080
  },
  "preview_url": null,
  "is_compliant": 0,
  "created_at": "2025-11-30T12:00:00Z"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Design not found"
}
```

**Example:**
```bash
curl http://localhost:8000/api/designs/1
```

---

### Export Design

Export a design in specified format.

**Endpoint:** `GET /api/designs/{id}/export?format={format}`

**Path Parameters:**
- `id` (integer): Design ID

**Query Parameters:**
- `format` (string): Export format - `png`, `jpg`, `svg`, or `pdf`

**Response:** `200 OK` (binary file)
- Content-Type: `image/png`, `image/jpeg`, `image/svg+xml`, or `application/pdf`
- Content-Disposition: `attachment; filename=design_1.png`

**Example:**
```bash
# Download as PNG
curl -O -J http://localhost:8000/api/designs/1/export?format=png

# Download as JPG
curl -O -J http://localhost:8000/api/designs/1/export?format=jpg

# Download as SVG
curl -O -J http://localhost:8000/api/designs/1/export?format=svg
```

---

## Guidelines

### Upload Guideline

Upload and process brand guideline document.

**Endpoint:** `POST /api/guidelines/upload`

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file` (file): PDF or image file (max 10MB)

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Brand_Guidelines_2025.pdf",
  "file_url": null,
  "colors": ["#0066cc", "#ff6600", "#00cc66"],
  "fonts": ["Helvetica Neue", "Arial"],
  "logo_urls": [],
  "created_at": "2025-11-30T12:00:00Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/guidelines/upload \
  -F "file=@/path/to/brand_guidelines.pdf"
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/guidelines/upload', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

---

### List Guidelines

Get all uploaded brand guidelines.

**Endpoint:** `GET /api/guidelines`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Brand_Guidelines_2025.pdf",
    "file_url": null,
    "colors": ["#0066cc", "#ff6600", "#00cc66"],
    "fonts": ["Helvetica Neue", "Arial"],
    "logo_urls": [],
    "created_at": "2025-11-30T12:00:00Z"
  }
]
```

**Example:**
```bash
curl http://localhost:8000/api/guidelines
```

---

### Get Guideline

Get a specific guideline by ID.

**Endpoint:** `GET /api/guidelines/{id}`

**Path Parameters:**
- `id` (integer): Guideline ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Brand_Guidelines_2025.pdf",
  "file_url": null,
  "colors": ["#0066cc", "#ff6600", "#00cc66"],
  "fonts": ["Helvetica Neue", "Arial", "Georgia"],
  "logo_urls": [],
  "created_at": "2025-11-30T12:00:00Z"
}
```

---

## Compliance

### Check Compliance

Check if design meets platform requirements.

**Endpoint:** `POST /api/compliance/check`

**Request Body:**
```json
{
  "design_id": 1,
  "platform": "meta"
}
```

**Parameters:**
- `design_id` (integer, required): ID of design to check
- `platform` (string, required): Platform to check against - `meta`, `google`, or `linkedin`

**Response:** `200 OK`
```json
{
  "design_id": 1,
  "platform": "meta",
  "is_compliant": false,
  "issues": [
    {
      "type": "dimensions",
      "message": "Expected 1080x1080, got 800x800",
      "severity": "error"
    },
    {
      "type": "text_content",
      "message": "No text found in design",
      "severity": "warning"
    }
  ],
  "checked_at": "2025-11-30T12:00:00Z"
}
```

**Issue Severity Levels:**
- `error`: Must be fixed (design is non-compliant)
- `warning`: Should be reviewed (design may be rejected)

**Example:**
```bash
curl -X POST http://localhost:8000/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "design_id": 1,
    "platform": "meta"
  }'
```

---

## Platform Specifications

### Meta (Facebook/Instagram)

**Square (1:1)**
- Dimensions: 1080×1080 px
- File size: Max 30MB
- Text ratio: < 20% recommended

**Landscape (16:9)**
- Dimensions: 1200×628 px
- File size: Max 30MB

**Portrait (4:5)**
- Dimensions: 1080×1350 px
- File size: Max 30MB

**Story (9:16)**
- Dimensions: 1080×1920 px
- File size: Max 30MB

### Google Ads

**Square**
- Dimensions: 1200×1200 px
- File size: Max 150KB

**Landscape**
- Dimensions: 1200×628 px
- File size: Max 150KB

### LinkedIn

**Square**
- Dimensions: 1200×1200 px
- File size: Max 5MB

**Landscape**
- Dimensions: 1200×627 px
- File size: Max 5MB

---

## Error Responses

All endpoints may return these error responses:

**400 Bad Request**
```json
{
  "detail": "Invalid request parameters"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limits

**Development:** No rate limits

**Production (future):**
- 100 requests per minute per IP
- 1000 requests per day per user

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can:
- See all endpoints
- Try API calls directly
- View request/response schemas
- Download OpenAPI spec

---

## SDK Examples

### JavaScript/TypeScript

```javascript
// services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const generateDesign = async (data) => {
  const response = await axios.post(`${API_URL}/designs/generate`, data);
  return response.data;
};

export const getDesigns = async () => {
  const response = await axios.get(`${API_URL}/designs`);
  return response.data;
};

export const uploadGuideline = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_URL}/guidelines/upload`, formData);
  return response.data;
};
```

### Python

```python
import requests

API_URL = "http://localhost:8000/api"

def generate_design(prompt, platform, format):
    response = requests.post(
        f"{API_URL}/designs/generate",
        json={
            "prompt": prompt,
            "platform": platform,
            "format": format
        }
    )
    return response.json()

def get_designs():
    response = requests.get(f"{API_URL}/designs")
    return response.json()
```

---

## Webhooks (Future)

Webhook support coming soon for:
- Design generation completion
- Guideline processing completion
- Export ready for download

---

**Last Updated:** 2025-11-30  
**API Version:** 1.0.0
