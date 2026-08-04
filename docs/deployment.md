# PawPal+ Deployment Guide

## Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Configuration](#configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [Next Steps](#next-steps)

---

Complete setup for running Flask backend + React frontend locally and deploying to production.

## Local Development

### Step 1: Backend Setup (Flask)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask API server
python flask_api.py
```

Flask runs on `http://localhost:5000`

Test it:
```bash
curl http://localhost:5000/api/health
# Expected: {"status": "ok", "service": "PawPal+ API"}
```

### Step 2: Frontend Setup (React)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

React opens at `http://localhost:3000`

**Frontend calls Flask at:** `http://localhost:5000` (configured in App.js)

---

## What the App Does

**Three main features:**

1. **Task Manager**
   - Add tasks to pets
   - Track by pet, time, priority
   - Stores in memory (can extend to database)

2. **Recommendation Engine**
   - Enter a care recommendation
   - Choose retrieval mode (Heuristic or Groq API)
   - See AI validation + confidence score

3. **A/B Test**
   - Compare both modes side-by-side
   - See which retrieval method is better
   - Useful for portfolio/interviews

---

## Production Deployment

### Option 1: Simple Local + GitHub Pages

**Backend:** Run locally or deploy to free tier service
**Frontend:** Deploy to GitHub Pages

#### Deploy Frontend to GitHub Pages

```bash
cd frontend

# Update package.json homepage to your repo
# "homepage": "https://YOUR-USERNAME.github.io/applied-ai-petcare-system"

npm run build
npm run deploy
```

**Result:** Frontend lives at `https://ikaera.github.io/applied-ai-petcare-system`

#### Backend - Deploy to Free Service

Choose one:

**Option A: Render.com (recommended)**
```bash
# 1. Create account at render.com
# 2. Connect your GitHub repo
# 3. Create new Web Service
# 4. Build command: pip install -r requirements.txt
# 5. Start command: python flask_api.py
# 6. Environment: Add GROQ_API_KEY from your .env
# 7. Deploy!
```

**Option B: Railway.app**
```bash
# 1. Create account at railway.app
# 2. Connect GitHub
# 3. Add GROQ_API_KEY in Variables
# 4. Deploy!
```

**Option C: Heroku (no free tier anymore)**
Use Render or Railway instead.

### Option 2: Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY flask_api.py .
COPY src/ src/
COPY pawpal_system.py .
COPY knowledge_base.json .

EXPOSE 5000
CMD ["python", "flask_api.py"]
```

Then deploy to Docker Hub, Railway, or Render.

---

## Configuration

### Backend URL

The React frontend needs to know where Flask is running.

**Local:** Default is `http://localhost:5000` (hardcoded in App.js)

**Production:** Update App.js:
```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

Set environment variable before building:
```bash
cd frontend
REACT_APP_API_URL=https://your-backend-url.herokuapp.com npm run build
```

### CORS Settings

Flask has CORS enabled for all origins (Flask-CORS).

For production, restrict to your domain:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://ikaera.github.io"]
    }
})
```

---

## Testing

### Test Flask API

```bash
# Health check
curl http://localhost:5000/api/health

# Get pets
curl http://localhost:5000/api/pets

# Get tasks
curl http://localhost:5000/api/tasks

# Add task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"pet": "Mochi", "title": "Walk", "time": "09:00", "priority": "high"}'

# Get recommendation
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"pet": "Mochi", "recommendation": "Feed kibble", "mode": "heuristic"}'

# Compare modes
curl -X POST http://localhost:5000/api/compare \
  -H "Content-Type: application/json" \
  -d '{"pet": "Mochi", "recommendation": "Feed kibble"}'
```

### Test React Locally

Visit `http://localhost:3000` in browser. Try:
- Adding a task
- Getting a recommendation
- Comparing modes

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| React can't connect to Flask | Check Flask is running on 5000 |
| CORS error | Flask needs `flask-cors` enabled |
| `npm install` fails | Delete `node_modules` and try again |
| Build fails | Check Node version: `node --version` (need 14+) |
| Env var not loaded | Restart React dev server after setting var |

---

## File Structure

```
.
├── flask_api.py                 # Backend server
├── requirements.txt             # Python dependencies
├── pawpal_system.py             # Task scheduler
├── knowledge_base.json          # AI knowledge base
├── src/ai/                      # AI components
│   ├── retriever.py
│   ├── validator.py
│   ├── integrator.py
│   └── agentic_planner.py
│
└── frontend/                    # React app
    ├── package.json
    ├── README.md
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        ├── App.css
        ├── index.js
        └── components/
            ├── TaskManager.js
            ├── RecommendationEngine.js
            └── ABComparison.js
```

---

## Next Steps

1. **Local:** Run both Flask and React, test features
2. **Deploy Backend:** Choose Render or Railway
3. **Deploy Frontend:** GitHub Pages
4. **Test Production:** Visit deployed URL
5. **Share:** Send link to reviewers/interviewers

---

## Portfolio Tips

When showing this to interviewers:

- **Architecture:** React (frontend) + Flask (backend) separation of concerns
- **API Design:** RESTful endpoints for tasks and recommendations
- **State Management:** Simple React hooks (not Redux)
- **AI Integration:** Shows understanding of dual-mode retrieval
- **Full Stack:** Demonstrates both frontend and backend skills

## Quick Demo Commands

```bash
# Terminal 1: Backend
pip install -r requirements.txt
python flask_api.py

# Terminal 2: Frontend
cd frontend
npm install
npm start

# Browser: http://localhost:3000
```

Done! 🚀
