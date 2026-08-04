# PawPal+ Applied AI System

An intelligent pet care task scheduler enhanced with retrieval-augmented generation (RAG), automated validation, and multi-step reasoning.

**Quick Start:** [Installation](#installation) • [Run](#usage) • [Examples](#examples) • [Tests](#testing--evaluation) • [React Frontend](#full-stack-ui-flask--react)

---

## Table of Contents

**Getting Started:**
- [Quick Reference](#quick-reference) — Common commands
- [5-Minute Setup](#5-minute-setup) — Fast local setup
- [Installation](#installation) — Full installation steps

**Understanding the System:**
- [Overview](#overview) — What is PawPal+
- [The Problem & Solution](#the-problem--solution) — Why it matters
- [AI Features](#ai-features) — Core AI components
- [Full-Stack UI: Flask + React](#full-stack-ui-flask--react) — Web interface

**Using & Testing:**
- [Usage](#usage) — How to run (4 options)
- [Examples](#examples) — Demo walkthroughs
- [Testing](#testing--evaluation) — Test suite & evaluation
- [Dual-Mode Retrieval](#dual-mode-retrieval-new) — Heuristic vs Groq API

**Advanced:**
- [Design Decisions](#design-decisions) — Architecture choices
- [Reflection](#reflection) — AI collaboration & learning
- [Documentation](#documentation) — All technical docs

**For Grading:**
- [Rubric Verification](RUBRIC_VERIFICATION.md) — 29/29 points verified

---

## Overview

**PawPal+** is a pet care task scheduler enhanced with AI. It helps pet owners organize multiple pets' care tasks into realistic daily schedules while ensuring recommendations are safe, fair, and knowledge-backed.

### In Simple Terms

Think of PawPal+ as a smart assistant that:
1. **Knows pet care** - Has a knowledge base of 15 pet care documents
2. **Checks safety** - Validates every recommendation (medical tasks need vet docs)
3. **Explains decisions** - Shows confidence scores so you know when to trust it
4. **Handles complexity** - Works with multiple pets and conflicting schedules

**Try it:**
```bash
python main.py              # See it in action
python ab_testing.py        # Compare heuristic vs AI modes
python comparison_demo.py   # See how it ranks documents
```

---

## The Problem & Solution

### The Challenge
Pet owners with multiple pets struggle with:
- Scheduling conflicts (dog walk vs. cat feeding at same time)
- Time management (fitting tasks into available time)
- Safety (ensuring recommendations are veterinarian-approved)
- Fairness (avoiding generic "all dogs need X" advice)

### The Solution
An AI system that:
1. **Retrieves** knowledge from curated pet care documents
2. **Validates** recommendations for safety and fairness
3. **Plans** multi-step schedules with transparent reasoning
4. **Scores** confidence so users know when to trust the system

**Example:** "Morning walk for Mochi" → Retrieves "Dog Exercise Requirements" + "Dog Health Basics" → Validates it's appropriate for this dog's age/breed → Returns schedule with 95% confidence

---

## AI Features

### 1. RAG Retrieval
Searches 15 curated pet care documents before recommending. Retrieves 3 most relevant docs per task, species-specific (dogs vs. cats).
**Implementation:** [src/ai/retriever.py](src/ai/retriever.py)

### 2. Validation Guardrails
Checks recommendations for safety, completeness, fairness. Flags medical tasks without vet docs, detects bias, provides confidence scores (0.0-1.0).
**Implementation:** [src/ai/validator.py](src/ai/validator.py)

### 3. Agentic Planning
6-step reasoning pipeline: constraints → priorities → conflicts → optimization → validation → execution. Each step has confidence tracking.
**Implementation:** [src/ai/agentic_planner.py](src/ai/agentic_planner.py)

### 4. Bias Detection
Flags over-generalizations ("all dogs need X"). Ensures individual pet context considered. Suggests personalized improvements.
**Implementation:** [src/ai/validator.py](src/ai/validator.py)

**Integrated:** All features work together in the main workflow, not as isolated demos.

---

## Full-Stack UI: Flask + React

A modern web interface for interacting with the AI system.

### What You Get

**Backend:** Flask REST API with 7 endpoints
- Task management (add, list, complete)
- Single recommendations with validation
- A/B comparison of retrieval modes
- Daily plan generation

**Frontend:** React UI with 3 feature tabs
1. **Task Manager** - Schedule tasks for multiple pets
2. **Recommendation Engine** - Get AI recommendations (choose retrieval mode)
3. **A/B Test** - Compare Heuristic vs Groq API side-by-side

### Quick Start

**5-minute setup:**
```bash
# Terminal 1: Backend
pip install -r requirements.txt
python flask_api.py

# Terminal 2: Frontend
cd frontend
npm install
npm start
```

Opens at `http://localhost:3000` (React) connected to `http://localhost:5000` (Flask)

### Architecture

```
React UI (http://localhost:3000)
    ↓ axios calls
Flask API (http://localhost:5000)
    ↓
Python AI System (retriever, validator, integrator)
```

### Deployment

**Frontend:** GitHub Pages  
**Backend:** Render.com or Railway (free tier)

See [docs/deployment.md](docs/deployment.md) for full production setup.

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed system design.

Quick overview:
```
Input → Scheduler → AI Integrator {
  RAG Retriever (15 docs)
  Validator (5 rules + bias detection)
  Agentic Planner (6 steps)
} → Output with confidence scores
```

---

## Installation

### Prerequisites
- **Python** 3.8+
- **pip** (Python package manager)
- **Node.js** 14+ (for React frontend, optional)
- **npm** (comes with Node.js)

### Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/ikaera/applied-ai-petcare-system.git
cd applied-ai-petcare-system
```

**2. Create a virtual environment**

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Verify installation**
```bash
pytest tests/ -v
# Expected: 83/83 tests passing
```

### Frontend Setup (Optional)

To use the React UI:

**5. Install Node dependencies**
```bash
cd frontend
npm install
```

**6. Done!** Now you can run React + Flask together (see [Quick Reference](#quick-reference))

---

## Quick Reference

### Prerequisites Met?
```powershell
# Check Python
python --version          # Need 3.8+

# Check Node.js (for React - optional)
node --version            # Need 14+

# Activate virtual environment (always do this first!)
.venv\Scripts\activate    # Windows
# OR
source .venv/bin/activate # macOS/Linux
```

### Essential Commands

```powershell
# ALWAYS activate venv first:
.venv\Scripts\activate

# Tests
pytest tests/ -v                          # All 83 tests (100% passing)

# Command-Line Demos
python main.py                            # RAG + validation demo
python agentic_demo.py                    # 6-step reasoning pipeline
python ab_testing.py                      # Compare retrieval modes

# Web UIs (pick one)
streamlit run app.py                      # Streamlit UI (http://localhost:8501)
python flask_api.py                       # Flask backend (http://localhost:5000)
cd frontend && npm start                  # React UI (http://localhost:3000)
```

---

## 5-Minute Setup

**Prerequisites:** Python 3.8+, Node.js 14+ (optional for React)

### Option A: Command-Line Only (Fastest)

```powershell
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run any demo
python main.py
pytest tests/ -v

# Done! No UI needed, just terminal output
```

### Option B: Streamlit Web UI

```powershell
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit
streamlit run app.py

# Opens http://localhost:8501
# Shows: Task manager, schedule generator, validation results
```

### Option C: Flask + React (Full-Stack) ⭐ Recommended

```powershell
# Terminal 1: Backend
.venv\Scripts\activate
python flask_api.py
# Runs on http://localhost:5000

# Terminal 2: Frontend
cd frontend
npm install                    # First time only
npm start
# Opens http://localhost:3000
```

**Features shown:**
- Task Manager (add/view tasks)
- Recommendation Engine (test with chosen retrieval mode)
- A/B Test (compare Heuristic vs Groq API)
- Live validation with confidence scores

---

## Usage

### Option 1: Command-Line Demo

Run the complete system with example data:

```powershell
# Activate virtual environment first!
.venv\Scripts\activate

# Then run demo
python main.py
```

**Output:**
- Daily schedule table with task priorities
- Retrieved documents for each task
- Validation results (PASS/REVIEW/BIASED)
- System reliability metrics
- Confidence scores (0.0–1.0)

### Option 2: Agentic Planning Demo

See the 6-step reasoning pipeline with confidence tracking:

```powershell
.venv\Scripts\activate
python agentic_demo.py
```

**Output:**
- Step-by-step reasoning trace
- Confidence scores for each step
- Overall plan viability score
- Interaction log with detailed reasoning

### Option 3: Streamlit Web UI

Interactive web interface for exploring the system:

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Run Streamlit
streamlit run app.py
```

Opens at: **http://localhost:8501**

**Features:**
- Enter pet information and constraints
- Add care tasks (feeding, exercise, medical, etc.)
- Generate optimal daily schedule
- View validation results
- See confidence scores
- Explore retrieved documents

### Option 4: Flask + React (Full-Stack) ⭐ **Recommended for Portfolio**

Professional modern UI with three feature tabs:

```powershell
# Terminal 1: Start Flask backend
.venv\Scripts\activate
python flask_api.py
# Runs on http://localhost:5000

# Terminal 2: Start React frontend (new terminal)
cd frontend
npm install              # First time only
npm start
```

Opens at: **http://localhost:3000**

**Three Feature Tabs:**

| Tab | Description |
|-----|-------------|
| **Task Manager** | Add tasks, set time/priority, manage multiple pets |
| **Recommendation Engine** | Test recommendations with chosen retrieval mode (Heuristic or Groq API), see validation + confidence |
| **A/B Test** | Compare results from both retrieval modes side-by-side |


---

## Examples

### Example 1: Basic Demo
```powershell
.venv\Scripts\activate
python main.py
```

**Input:** 2 pets (dog + cat), 8 tasks, 90 min available
**Output:** Schedule with retrieval docs, validation results, confidence scores

**What it shows:** RAG retrieval working, validation active, confidence scores transparent

---

### Example 2: Agentic Reasoning
```powershell
.venv\Scripts\activate
python agentic_demo.py
```

**Output:** 6-step reasoning trace with confidence per step, overall viability score

**What it shows:** Multi-step planning with transparency, real issues detected (conflicts, validation warnings)

---

### Example 3: Full Test Suite
```bash
pytest tests/ -v
# Result: 83/83 passing (100%)
```

**Coverage:** Retriever (6), Validator (13), Integrator (5), End-to-End (1), Scheduler (47)

**What it shows:** All components working, bias detection included, full integration tested

---

## Testing & Evaluation

**83 tests, 100% passing.** See [docs/testing.md](docs/testing.md) for full strategy.

```bash
pytest tests/ -v
```

**Test breakdown:**
- RAG Retriever: 6/6 ✓
- Validator (+ bias detection, combination tests): 13/13 ✓
- AI Integrator: 5/5 ✓
- End-to-End: 1/1 ✓
- Original Scheduler: 47/47 ✓

**Key verifications:**
- Medical tasks without vet docs → REVIEW (not PASS)
- Safe tasks → PASS with high confidence
- Biased recommendations → flagged with suggestions
- All components work together

---

## Reliability & Guardrails

### How It Works

Medical task without vet docs:
```
Input: "Evening meds" for Mochi
Result: ⚠ REVIEW (0.70 confidence)
Reason: Missing veterinary documentation
Action: User must confirm with vet before proceeding
```

Safe task:
```
Input: "Feeding" for Whiskers
Result: ✓ PASS (1.00 confidence)
Reason: Safe, species-appropriate, well-documented
Action: Proceed immediately
```

Biased recommendation:
```
Input: "All dogs need 30 minute walks"
Result: ⚠ BIASED (0.80 confidence)
Reason: Over-generalization, missing individual context
Action: Improve to "Based on Mochi's age and breed, 30 minute walks are appropriate"
```

---

## Deployment to Production

### Option 1: React Frontend on GitHub Pages (Free)

**1. Build the React app:**
```powershell
cd frontend
npm run build
```

**2. Deploy to GitHub Pages:**
```powershell
npm run deploy
```

**Result:** Frontend lives at `https://ikaera.github.io/applied-ai-petcare-system`

**Note:** Update `frontend/package.json` homepage if your repo is different:
```json
"homepage": "https://YOUR-USERNAME.github.io/applied-ai-petcare-system"
```

### Option 2: Flask Backend on Render.com (Free Tier)

**1. Create account:** https://render.com

**2. Connect GitHub repo:**
- Sign in with GitHub
- Create new "Web Service"
- Select your repo

**3. Configure deployment:**
```
Build Command: pip install -r requirements.txt
Start Command: python flask_api.py
Environment Variables:
  - GROQ_API_KEY=your_actual_key_here
```

**4. Deploy:**
- Render automatically deploys on git push
- Get your URL: `https://your-app-name.onrender.com`

### Option 3: Backend on Railway.app (Free Tier)

**1. Create account:** https://railway.app

**2. Connect GitHub:**
- Login with GitHub
- Create new project from repo

**3. Add environment variable:**
- Add `GROQ_API_KEY=your_actual_key_here`

**4. Deploy:**
- Railway auto-deploys
- Get URL from dashboard

### Update React to Call Deployed Backend

Once backend is deployed, update React to call it:

**In `frontend/src/App.js`:**
```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'https://your-app-name.onrender.com';
```

**Before building, set environment variable:**
```powershell
$env:REACT_APP_API_URL="https://your-backend-url.com"
npm run build
```

### Complete Deployment Checklist

✅ Backend deployed to Render/Railway  
✅ Frontend deployed to GitHub Pages  
✅ React points to deployed backend  
✅ GROQ_API_KEY set in backend environment  
✅ CORS enabled in Flask (already configured)  
✅ Both services accessible from browser  

**Full details:** See [docs/deployment.md](docs/deployment.md)

---

## Design Decisions

See [ai_interactions.md](ai_interactions.md) for detailed implementation reasoning.

**Key choices:**
1. **Keyword-based retrieval** (not embeddings) → Simpler, sufficient for structured tasks
2. **Rule-based validation** (not ML) → Transparent, safe for pet health
3. **Fixed 6-step planning** (not dynamic agents) → More debuggable, matches scope
4. **Static knowledge base** (not APIs) → Controlled, private, consistent

**Trade-offs documented** in [ai_interactions.md](ai_interactions.md) and [docs/extensions-roadmap.md](docs/extensions-roadmap.md)

---

## Dual-Mode Retrieval (NEW)

The system now supports **two retrieval modes** to balance speed and semantic understanding:

### Mode 1: Heuristic (Keyword-Based)
- **Speed:** Fast, no API latency
- **Dependencies:** None (no API key needed)
- **Best for:** Development, testing, simple queries
- **How:** TF-IDF keyword matching with stop-word filtering

```python
from src.ai.integrator import AISchedulingIntegrator

# Heuristic mode (default)
integrator = AISchedulingIntegrator(retriever_mode="heuristic")
```

### Mode 2: Groq API (Semantic)
- **Speed:** Slightly slower (API call overhead)
- **Dependencies:** Groq API key (free from console.groq.com)
- **Best for:** Complex queries, semantic understanding, production
- **How:** Groq LLM ranks documents by relevance, falls back to heuristic if API fails

```python
# Groq API mode (with fallback)
integrator = AISchedulingIntegrator(retriever_mode="groq")
```

### Setup for Groq API

1. Get free API key: https://console.groq.com (no credit card required)
2. Copy `.env.example` to `.env`
3. Add your key: `GROQ_API_KEY=your_key_here`
4. Run: `pip install -r requirements.txt` (includes groq, python-dotenv)

### Comparison & Testing

Three tools included to help you choose and compare:

1. **`comparison_demo.py`** - Side-by-side comparison of both modes
   ```bash
   python comparison_demo.py
   ```

2. **`groq_mode_demo.py`** - Full system walkthrough using Groq API
   ```bash
   python groq_mode_demo.py
   ```

3. **`ab_testing.py`** - A/B test both modes on real scenarios
   ```bash
   python ab_testing.py
   ```

### Why Two Modes?

| Scenario | Heuristic | Groq API |
|----------|-----------|----------|
| Quick prototype | ✓ | |
| No API key available | ✓ | |
| Development/testing | ✓ | |
| Complex semantic queries | | ✓ |
| Production with fallback | ✓ | ✓ |
| Response time critical | ✓ | |

### Tests

Both modes thoroughly tested (11 new integration tests):
- Fallback behavior when API unavailable
- Consistent output format between modes
- Validation works with both retrievers
- Metrics include mode information

Run: `pytest tests/test_groq_integration.py -v`

---

## Reflection

**What surprised me:** Simplicity wins. Keyword retrieval works better than embeddings for structured pet care. Rule-based validation more trustworthy than ML for safety decisions.

**What I learned:** Responsible AI means transparency and safety over raw accuracy. Systems thinking matters (integration, testing, monitoring). Users care about why, not just what.

**Effective AI collaboration:** Used AI well for architecture and testing strategy. Rejected over-engineered suggestions when simpler solutions fit better.

**Full reflection:** See [reflection.md](reflection.md) for system design thinking.

---

## Documentation

**Technical References:**
- [docs/architecture.md](docs/architecture.md) — System design, Mermaid diagram, components
- [docs/testing.md](docs/testing.md) — Test strategy & 83-test suite
- [docs/deployment.md](docs/deployment.md) — Production deployment (Flask + React)
- [docs/extensions-roadmap.md](docs/extensions-roadmap.md) — Future features
- [docs/model_card.md](docs/model_card.md) — Responsible AI & limitations

**Deep Dives:**
- [ai_interactions.md](ai_interactions.md) — Implementation decisions & design trade-offs
- [reflection.md](reflection.md) — System design thinking & AI collaboration
- [RUBRIC_VERIFICATION.md](RUBRIC_VERIFICATION.md) — Rubric checklist (29/29 points)

**Presentations:**
- [PRESENTATION.md](PRESENTATION.md) — Demo Day pitch (speaker notes)

---

## Portfolio

**What This Project Demonstrates:**

I build AI systems that are **trustworthy, transparent, and genuinely useful**—not just technically impressive.

- **Full-Stack Development:** Flask backend + React frontend, REST API, responsive UI
- **Responsible AI:** Confidence scores, guardrails, honest about uncertainty
- **Systems Thinking:** Integration + testing + monitoring + continuous improvement
- **Practical Problem-Solving:** Chose simplicity over over-engineering (keyword retrieval, rule-based validation)
- **Quality & Reliability:** 83 tests (100% passing), modular architecture
- **User-Centric Design:** Built for real pet owners, interactive web UI
- **AI/ML Integration:** Dual-mode retrieval (heuristic + semantic), validation guardrails
- **Effective AI Collaboration:** Used Claude well for architecture & strategy, rejected over-engineered suggestions
- **Modern Web Stack:** React hooks, Flask blueprints, CORS, responsive CSS

**GitHub:** https://github.com/ikaera/applied-ai-petcare-system

---

## License

Educational and portfolio purposes.
