# PawPal+ React Frontend

Simple React UI for the PawPal+ AI system. Communicates with Flask API backend.

## Features

- **Task Manager** - Add and track pet care tasks
- **Recommendation Engine** - Get AI recommendations with validation
- **A/B Test** - Compare heuristic vs Groq API retrieval modes

## Setup

### Backend (Flask API)

```bash
# Install Python dependencies
pip install -r ../requirements.txt

# Run Flask server
python ../flask_api.py
# API runs on http://localhost:5000
```

### Frontend (React)

```bash
# Install dependencies
npm install

# Start development server
npm start
# Opens http://localhost:3000
```

## Build & Deploy to GitHub Pages

```bash
npm run build
npm run deploy
```

Deploys to `https://ikaera.github.io/applied-ai-petcare-system`

## API Endpoints

The React frontend calls these Flask endpoints:

- `GET /api/health` - Health check
- `GET /api/pets` - Get all pets
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Add new task
- `POST /api/recommend` - Get single recommendation
- `POST /api/compare` - Compare both retrieval modes
- `POST /api/plan` - Generate daily plan

## Environment Variables

Set `REACT_APP_API_URL` to point to Flask backend:

```bash
REACT_APP_API_URL=http://localhost:5000
```

Default: `http://localhost:5000`

## Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── App.js
│   ├── App.css
│   └── components/
│       ├── TaskManager.js
│       ├── TaskManager.css
│       ├── RecommendationEngine.js
│       ├── RecommendationEngine.css
│       ├── ABComparison.js
│       └── ABComparison.css
└── package.json
```
