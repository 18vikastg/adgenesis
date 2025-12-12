# AdGenesis - Quick Start Guide

## ✨ Generate Unlimited Ads for FREE!

AdGenesis uses a custom fine-tuned ML model to generate professional ad designs without any OpenAI costs.

## 🚀 Start All Services (ONE COMMAND!)

```bash
cd /home/vikas/Desktop/adgenesis
./run_all.sh
```

This automatically starts:
- 🤖 ML Service (port 8001)
- 🔧 Backend (port 8000)
- 🎨 Frontend (port 3000)

**Browser will open at http://localhost:3000**

Press `Ctrl+C` to stop all services.

---

## 🎯 How to Use

### 1. Open the App
Go to http://localhost:3000 and click **"Design Studio"**

### 2. Generate a Design
Enter any of these prompts:
- "Create a tech startup ad"
- "Create a fashion sale ad"  
- "Create a food delivery ad"
- "Create a business presentation"
- "Create a holiday discount ad"

### 3. Click "Generate Design"
Watch your ad appear in seconds!

### 4. Edit & Export
- **Edit**: Click to modify text and elements
- **Export**: Download as PNG image

---

## 🎨 Available Themes

The AI automatically detects keywords and applies these professional themes:

| Keyword | Background | Accent | Best For |
|---------|-----------|--------|----------|
| **tech, startup, AI, innovation** | Dark Blue (#1a1a2e) | Bright Blue (#3b82f6) | Tech companies, SaaS |
| **fashion, style, clothing** | Pink (#ff6b9d) | Yellow (#ffe66d) | Fashion brands, retail |
| **sale, discount, offer** | Red (#dc2626) | Yellow (#fbbf24) | Promotions, deals |
| **business, corporate, professional** | Navy (#1e3a8a) | Gold (#fbbf24) | B2B, consulting |
| **food, restaurant, dining** | Orange (#f97316) | Green (#22c55e) | Food delivery, restaurants |
| **default** | Purple (#7c3aed) | Pink (#ec4899) | General purpose |

---

## 🛠️ Manual Startup (Alternative)

If you prefer running services separately:

### Terminal 1 - ML Service
```bash
cd /home/vikas/Desktop/adgenesis
source backend/venv/bin/activate
cd ml_pipeline
python serve.py --model gpt2
```

### Terminal 2 - Backend  
```bash
cd /home/vikas/Desktop/adgenesis/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Terminal 3 - Frontend
```bash
cd /home/vikas/Desktop/adgenesis/frontend
npm start
```

---

## 🔧 Troubleshooting

### Port Already in Use?
```bash
lsof -ti:8001 | xargs kill -9  # Stop ML service
lsof -ti:8000 | xargs kill -9  # Stop backend
lsof -ti:3000 | xargs kill -9  # Stop frontend
```

### Check Service Status
```bash
curl http://localhost:8001/health  # ML service
curl http://localhost:8000/health  # Backend
curl http://localhost:3000         # Frontend
```

### View Logs
```bash
tail -f /tmp/ml_service.log   # ML service logs
tail -f /tmp/backend.log      # Backend logs  
tail -f /tmp/frontend.log     # Frontend logs
```

### Canvas Shows Blank?
✅ **FIXED** in latest version! If you still see issues:
1. Check browser console (F12) for JavaScript errors
2. Verify backend is returning design data: `curl http://localhost:8000/api/designs`
3. Try generating a new design with a different prompt

### Export Shows Blank Image?
✅ **FIXED** in latest version! Export now properly renders:
- Background colors
- Text elements
- Rectangle shapes
- Proper scaling

---

## 📊 System Status

Check if everything is running:

```bash
# Quick health check
curl -s http://localhost:8001/health && echo "✅ ML Service OK"
curl -s http://localhost:8000/health && echo "✅ Backend OK"  
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend OK"
```

---

## 🎯 Example Prompts

Try these to see different themes:

**Tech Theme:**
- "Create a tech startup ad for cloud computing"
- "Create an AI innovation advertisement"
- "Create a SaaS platform promotion"

**Fashion Theme:**
- "Create a fashion sale ad for summer collection"
- "Create a clothing brand advertisement"
- "Create a luxury fashion promotion"

**Sale Theme:**
- "Create a 50% off sale ad"
- "Create a Black Friday discount advertisement"
- "Create a limited time offer promotion"

**Business Theme:**
- "Create a business consulting ad"
- "Create a professional services advertisement"
- "Create a corporate training promotion"

**Food Theme:**
- "Create a food delivery ad"
- "Create a restaurant promotion"
- "Create a healthy eating advertisement"

---

## 💡 Tips for Best Results

1. **Be Specific**: "Create a tech startup ad for AI tools" is better than just "tech ad"
2. **Include Keywords**: Use theme keywords (tech, fashion, sale, etc.) for automatic styling
3. **Keep it Simple**: Short, clear prompts work best
4. **Edit After**: Generate first, then use Edit mode to refine
5. **Try Multiple**: Generate several variations and pick your favorite

---

## 🆘 Need Help?

1. **Logs**: Always check `/tmp/*.log` files first
2. **Services**: Make sure all 3 services are running
3. **Ports**: Ensure ports 8000, 8001, 3000 are free
4. **Browser**: Try clearing cache or using incognito mode
5. **Restart**: Use `./run_all.sh` to restart everything fresh

---

## ✨ What's New (Latest Fixes)

### Canvas Rendering
- ✅ Manual object creation instead of loadFromJSON
- ✅ Proper scaling from 1080x1080 to 800x800 display
- ✅ Background colors render correctly
- ✅ All elements (text, shapes) display properly

### Export Functionality  
- ✅ PIL-based image rendering (was returning blank)
- ✅ Text rendered with proper fonts and colors
- ✅ Rectangles drawn with correct fills
- ✅ Background colors applied correctly
- ✅ SVG export with proper elements

### ML Model
- ✅ Fallback design generator with 6 themes
- ✅ Keyword detection for automatic styling
- ✅ Professional color schemes
- ✅ Consistent layout (headline 25%, subtext 45%, CTA 65%)

---

## 🎉 You're Ready!

Run `./run_all.sh` and start creating amazing ads! 🚀
