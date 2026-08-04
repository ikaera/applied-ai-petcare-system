# Quick Setup Guide

For detailed instructions, see [README.md](../README.md#installation).

---

## Prerequisites

- Python 3.8+
- Git
- Text editor (VS Code, etc.)

---

## Installation (5 minutes)

**1. Clone**
```bash
git clone https://github.com/ikaera/applied-ai-petcare-system.git
cd applied-ai-petcare-system
```

**2. Virtual Environment**

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**4. Install Frontend (Optional)**
```bash
cd frontend
npm install
```

**5. Verify Installation**
```bash
pytest tests/ -v
# Expected: 83/83 passing
```

---

## Running the System

**1. Command-line demo:**
```bash
python main.py
```

**2. Agentic reasoning demo:**
```bash
python agentic_demo.py
```

**3. Streamlit web UI:**
```bash
streamlit run app.py
# Opens: http://localhost:8501
```

**4. Flask + React (Full-Stack) ⭐**
```bash
# Terminal 1: Backend
python flask_api.py
# Runs on http://localhost:5000

# Terminal 2: Frontend
cd frontend
npm start
# Opens: http://localhost:3000
```

**5. Run all tests:**
```bash
pytest tests/ -v
# Expected: 83/83 passing
```

---

## Project Structure

```
├── README.md                 # Main documentation
├── QUICKSTART.md             # 5-min setup guide
├── DEPLOYMENT.md             # Production deployment
├── PRESENTATION.md           # Demo Day pitch
├── requirements.txt          # Python dependencies
├── knowledge_base.json       # 15 pet care documents
├── pawpal_system.py          # Original scheduler
├── main.py                   # Demo: RAG + validation
├── agentic_demo.py           # Demo: 6-step reasoning
├── app.py                    # Streamlit web UI
├── flask_api.py              # Flask REST API
│
├── src/ai/
│   ├── retriever.py          # RAG implementation
│   ├── validator.py          # Validation + bias detection
│   ├── integrator.py         # Component orchestration
│   └── agentic_planner.py    # Multi-step reasoning
│
├── tests/
│   ├── test_ai_system.py     # AI component tests (22)
│   ├── test_groq_integration.py # Dual-mode tests (11)
│   ├── test_agentic_planner.py # Planner tests (3)
│   └── test_pawpal.py        # Scheduler tests (47)
│
├── frontend/                 # React UI (http://localhost:3000)
│   ├── package.json
│   ├── public/index.html
│   └── src/
│       ├── App.js
│       ├── App.css
│       ├── index.js
│       └── components/
│           ├── TaskManager.js
│           ├── RecommendationEngine.js
│           └── ABComparison.js
│
└── docs/
    ├── architecture.md       # System design
    ├── testing.md            # Test strategy
    ├── setup-guide.md        # This file
    ├── extensions-roadmap.md # Future features
    ├── model_card.md         # Responsible AI
    └── workflow.md           # Development process
```

---

## Troubleshooting

**Issue:** Python not found
- **Fix:** Install Python 3.8+ from python.org

**Issue:** pip not found
- **Fix:** Use `python -m pip` instead

**Issue:** Tests fail
- **Fix:** Make sure virtual environment is activated and requirements installed

**Issue:** streamlit not found
- **Fix:** Run `pip install -r requirements.txt` again

---

## Next Steps

1. Run `python main.py` to see the system in action
2. Check `tests/` to understand component behavior
3. Read `README.md` for feature overview
4. See `docs/architecture.md` for system design
