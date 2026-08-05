# petcare - Applied AI System

An intelligent pet care task scheduler with a user-friendly interface, enhanced with retrieval-augmented generation (RAG), automated validation, and multi-step reasoning.

**Quick Start:** [Installation](#installation) • [Web App](#option-3-web-interface) • [Testing](#testing-the-web-app) • [Documentation](#documentation)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Reference](#quick-reference)
- [Usage](#usage)
  - [Web Interface](#option-3-web-interface)
  - [Command-Line](#option-1-command-line-demo)
  - [Agentic Planning](#option-2-agentic-planning-demo)
- [Testing the Web App](#testing-the-web-app)
- [AI Features](#ai-features)
- [Design Decisions](#design-decisions)
- [Documentation](#documentation)

---

## Overview

**petcare** is an intelligent pet care task manager that helps pet owners organize multiple pets' care tasks into realistic daily schedules. It combines a beautiful, user-friendly interface with AI-powered recommendations that are safe, fair, and knowledge-backed.

### Key Features

**For Pet Owners:**
- 📋 Track tasks across multiple pets (walks, feeding, meds, enrichment, grooming)
- ⏰ Schedule with smart conflict detection
- 🔔 Set priorities and optimize your daily plan
- 💾 Automatic data saving and loading
- 📱 Beautiful, intuitive web interface

**For Learning AI/Engineering:**
- RAG retrieval from 15 curated pet care documents
- Validation guardrails with confidence scores
- 6-step agentic planning pipeline
- Bias detection and fairness checks
- 83 comprehensive tests (100% passing)

### Try It Now

**Web Interface (Recommended):**
```bash
streamlit run app.py
# Opens at http://localhost:8501
```

**CLI Demos:**
```bash
python main.py              # See it in action
python ab_testing.py        # Compare heuristic vs AI modes
python comparison_demo.py   # See how it ranks documents
```

---

## Features

### 🎯 Core Functionality
- **Multi-Pet Support** - Manage unlimited pets with different species (dogs, cats, other)
- **Task Management** - Create tasks with title, time, duration, priority, category, and frequency
- **Smart Scheduling** - Organize tasks with time budgeting and conflict detection
- **Daily Planning** - Generate optimized schedules respecting your available time

### 🎨 User Interface
- **Beautiful Design** - Clean, intuitive interface with emoji indicators
- **Multiple Views** - Sort by time, priority, or filter by pet/status
- **Real-Time Updates** - Instant feedback on all actions
- **Help Built-In** - Expandable guides and testing information in the app
- **Responsive Layout** - Works on different screen sizes

### 💾 Data Management
- **Auto-Save** - Pets and tasks saved automatically to JSON
- **Persistent Storage** - Data survives app restarts
- **Clear Data** - One-click button to start fresh
- **Scrollable Lists** - Handle many tasks without clutter

### 🤖 AI Features
- **RAG Retrieval** - Searches 15 pet care documents for recommendations
- **Validation** - Ensures recommendations are safe and fair
- **Confidence Scores** - Shows how confident the system is
- **Conflict Detection** - Warns about overlapping tasks
- **Plan Optimization** - Fits high-priority tasks first in your available time

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
- Python 3.8+
- pip (Python package manager)

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

---

## Quick Reference

```bash
pytest tests/ -v              # Run all tests (83/83)
python main.py                # Basic demo (RAG + validation)
python agentic_demo.py        # 6-step reasoning trace
streamlit run app.py          # Web interface (http://localhost:8501)
```

---

## Usage

### Option 1: Command-Line Demo

Run the complete system with example data:
```bash
python main.py
```

**Output:**
- Daily schedule table with task priorities
- Retrieved documents for each task
- Validation results (PASS/REVIEW)
- System reliability metrics
- Confidence scores (0.0–1.0)

### Option 2: Agentic Planning Demo

See the 6-step reasoning pipeline with confidence tracking:
```bash
python agentic_demo.py
```

**Output:**
- Step-by-step reasoning trace
- Confidence scores for each step
- Overall plan viability score
- Interaction log with detailed reasoning

### Option 3: Web Interface

Interactive web interface for managing your pet care tasks:
```bash
streamlit run app.py
```

Opens in browser at `http://localhost:8501`

**Features:**
- ✨ Beautiful, intuitive interface
- 🐾 Manage multiple pets
- 📝 Create and organize tasks
- 🔍 Sort by time, priority, or filter
- ⚠️ Detect scheduling conflicts
- 📅 Generate optimized daily plans
- 💾 Automatic data saving
- 📖 Built-in help and testing guide

---

## Testing the Web App

### Quick Test (5 minutes)

1. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

2. **Add a pet:**
   - Name: "Max"
   - Species: "dog"
   - Click "➕ Add Pet"

3. **Add tasks:**
   - Title: "Morning Walk" | Time: 08:00 | Priority: High | Duration: 30 min
   - Title: "Lunch" | Time: 12:00 | Priority: High | Duration: 15 min

4. **Test features:**
   - ✅ Click "⏰ By Time" tab - tasks sorted by time
   - ✅ Click "🔴 By Priority" tab - tasks sorted by priority
   - ✅ Click "🔍 Detect Conflicts" - should show "No conflicts"
   - ✅ Click "📅 Generate Plan" - shows optimized schedule

5. **Verify data persists:**
   - Close browser
   - Reopen `http://localhost:8501`
   - All pets and tasks should still be there

### Full Testing

For comprehensive testing with detailed scenarios, edge cases, and verification steps:
- See **TESTING.md** for 20+ detailed test scenarios
- See **QUICKSTART_TESTING.md** for a quick reference
- See **VERIFICATION_CHECKLIST.md** for checkbox-based testing
- Built-in help in the app: Click "📖 Help & Testing Guide"

### What to Verify

| Feature | Expected Result |
|---------|-----------------|
| **Add Pet** | Pet appears in table, can add multiple pets |
| **Add Task** | Task shows with all details (time, priority, category, duration) |
| **Mark Complete** | Task shows ✅, recurring tasks create next occurrence |
| **Sort by Time** | Tasks ordered earliest → latest |
| **Sort by Priority** | High → Medium → Low priority tasks |
| **Filter** | Can filter by pet and completion status |
| **Detect Conflicts** | Shows ⚠️ warnings for overlapping tasks |
| **Find Slot** | Suggests next available time |
| **Generate Plan** | Shows which tasks fit in available time |
| **Data Saves** | Restart app and data still there |
| **UI is Clear** | No overlapping text, emojis display correctly |

---

## Examples

### Example 1: Basic Demo
```bash
python main.py
```

**Input:** 2 pets (dog + cat), 8 tasks, 90 min available
**Output:** Schedule with retrieval docs, validation results, confidence scores

**What it shows:** RAG retrieval working, validation active, confidence scores transparent

---

### Example 2: Agentic Reasoning
```bash
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
- [docs/architecture.md](docs/architecture.md) — System design & component interactions
- [docs/testing.md](docs/testing.md) — Test strategy & evaluation
- [docs/setup-guide.md](docs/setup-guide.md) — Detailed installation
- [docs/extensions-roadmap.md](docs/extensions-roadmap.md) — Future features
- [docs/model_card.md](docs/model_card.md) — Responsible AI & limitations
- [docs/workflow.md](docs/workflow.md) — Development process
- [ai_interactions.md](ai_interactions.md) — Implementation reasoning
- [reflection.md](reflection.md) — System design reflection

**For Presentations:**
- [PRESENTATION.md](PRESENTATION.md) — 5-7 min Demo Day pitch (speaker notes)

---

## Portfolio

**What This Project Demonstrates:**

I build AI systems that are **trustworthy, transparent, and genuinely useful**—not just technically impressive.

- **Responsible AI:** Confidence scores, guardrails, honest about uncertainty
- **Systems Thinking:** Integration + testing + monitoring + continuous improvement
- **Practical Problem-Solving:** Chose simplicity over over-engineering (keyword retrieval, rule-based validation)
- **Quality & Reliability:** 83 tests (100% passing), modular architecture
- **User-Centric Design:** Built for real pet owners, not just impressive demos
- **Effective AI Collaboration:** Used Claude well for architecture & strategy, rejected over-engineered suggestions

**GitHub:** https://github.com/ikaera/applied-ai-petcare-system

---

## License

Educational and portfolio purposes.
