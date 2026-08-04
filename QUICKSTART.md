# Quick Start: Local Development

Get the Flask + React app running in 5 minutes.

## Prerequisites

- Python 3.8+
- Node.js 14+ (`node --version`)
- Git

## Step 1: Backend Setup (Flask)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run Flask server
python flask_api.py
```

**Expected output:**
```
WARNING in flaskenv: ... (ignore this)
 * Running on http://127.0.0.1:5000
```

✓ **Backend is running on http://localhost:5000**

Leave this terminal open. Open a new terminal for frontend.

## Step 2: Frontend Setup (React)

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start React development server
npm start
```

**Expected:** Browser opens to `http://localhost:3000`

---

## What You'll See

### Tab 1: Task Manager
- Add tasks for Mochi or Luna
- Tasks have time, priority, pet name
- Real-time list updates

### Tab 2: Recommendations
- Pick a pet and a recommendation
- Choose retrieval mode (Heuristic or Groq)
- See validation result + confidence score

### Tab 3: A/B Test
- Compare both retrieval modes side-by-side
- Heuristic (keyword-based) vs Groq API (semantic)
- See which performs better

---

## Testing with curl

In a third terminal, test the API:

```bash
# Health check
curl http://localhost:5000/api/health

# Get pets
curl http://localhost:5000/api/pets

# Get tasks
curl http://localhost:5000/api/tasks

# Add a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"pet":"Mochi","title":"Lunch","time":"12:00","priority":"high"}'

# Get a recommendation
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"pet":"Mochi","recommendation":"Feed kibble","mode":"heuristic"}'
```

---

## Stop Running

**Backend:** Press `Ctrl+C` in Flask terminal
**Frontend:** Press `Ctrl+C` in React terminal

---

## Common Issues

| Issue | Fix |
|-------|-----|
| `npm: command not found` | Install Node.js from nodejs.org |
| React won't connect to Flask | Make sure Flask is running on port 5000 |
| Port 5000 already in use | Change Flask: `python flask_api.py --port 5001` |
| Port 3000 already in use | Kill process or use: `PORT=3001 npm start` |
| `ModuleNotFoundError` in Flask | Run `pip install -r requirements.txt` again |

---

## Next: Deploy to Production

Once you've tested locally, see `DEPLOYMENT.md` for:
- Deploying backend to Render/Railway
- Deploying frontend to GitHub Pages
- Configuring CORS
- Testing production build

---

## Architecture

```
Your Browser
     ↓
http://localhost:3000 (React)
     ↓
axios calls ↓
     ↓
http://localhost:5000 (Flask API)
     ↓
Python AI system (retriever, validator, integrator)
     ↓
Returns JSON
```

---

**Happy coding! 🚀**
