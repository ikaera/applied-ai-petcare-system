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

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Verify**
```bash
pytest tests/ -v
# Expected: 83/83 passing
```

---

## Running the System

**Command-line demo:**
```bash
python main.py
```

**Agentic reasoning demo:**
```bash
python agentic_demo.py
```

**Web interface:**
```bash
streamlit run app.py
# Opens: http://localhost:8501
```

**Run tests:**
```bash
pytest tests/ -v
```

---

## Project Structure

```
├── README.md                 # Main documentation
├── PRESENTATION.md           # Demo Day pitch
├── requirements.txt          # Dependencies
├── knowledge_base.json       # 15 pet care documents
├── pawpal_system.py          # Original scheduler
├── main.py                   # Demo: RAG + validation
├── agentic_demo.py           # Demo: 6-step reasoning
├── app.py                    # Streamlit web UI
│
├── src/ai/
│   ├── retriever.py          # RAG implementation
│   ├── validator.py          # Validation + bias detection
│   ├── integrator.py         # Component orchestration
│   └── agentic_planner.py    # Multi-step reasoning
│
├── tests/
│   ├── test_ai_system.py     # AI tests (22)
│   └── test_pawpal.py        # Scheduler tests (47)
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
