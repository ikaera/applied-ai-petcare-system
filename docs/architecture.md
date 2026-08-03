# System Architecture

## Overview

PawPal+ combines a scheduling engine with AI features. The system is modular: each component is independent and testable.

---

## Components

**Scheduler** (Original)
- Task management and prioritization
- Time budget optimization
- Conflict detection
- Data persistence

**RAG Retriever** (`src/ai/retriever.py`)
- Searches 15 curated pet care documents
- Returns top-3 relevant docs per task
- Species-specific (dogs vs. cats)
- TF-IDF keyword matching

**Validator** (`src/ai/validator.py`)
- 5 safety rules (medical, species-appropriate, etc.)
- Detects bias and over-generalizations
- Provides confidence scores (0.0-1.0)
- Suggests improvements

**Agentic Planner** (`src/ai/agentic_planner.py`)
- 6-step reasoning pipeline
- Confidence tracking per step
- Overall plan viability scoring
- Optional file logging (no side effects by default)

**Integrator** (`src/ai/integrator.py`)
- Combines all components
- Tracks metrics (validation rate, avg confidence, etc.)
- Logs interactions for transparency

---

## Data Flow

```
User Input
    ↓
Scheduler (generate base plan)
    ↓
AI Integrator
    ├─→ RAG Retriever (fetch knowledge)
    ├─→ Validator (check safety)
    └─→ Metrics (track quality)
    ↓
Enhanced Plan (with retrieval + validation + confidence)
    ↓
Output (Console, Web UI, or JSON)
```

---

## Design Principles

1. **Separation of Concerns** - Each component has one responsibility
2. **No Side Effects** - Logging is opt-in, tests don't create files
3. **Transparency** - Every decision is explained with confidence scores
4. **Testability** - Components are independent and injectable
5. **Extensibility** - Easy to swap or upgrade components

---

## Key Files

| File | Purpose |
|------|---------|
| `pawpal_system.py` | Original scheduler (Owner, Pet, Task, Scheduler) |
| `src/ai/retriever.py` | RAG knowledge base search |
| `src/ai/validator.py` | Safety checks + bias detection |
| `src/ai/agentic_planner.py` | Multi-step reasoning with logging |
| `src/ai/integrator.py` | Component orchestration |
| `knowledge_base.json` | 15 curated pet care documents |
| `tests/test_ai_system.py` | AI component tests (22 tests) |
| `tests/test_pawpal.py` | Scheduler tests (47 tests) |

---

## Why This Architecture?

- **Modularity:** Can use scheduler alone, or add AI features incrementally
- **Testing:** Each component tested independently + end-to-end
- **Reliability:** Validation + confidence scores + guardrails
- **Clarity:** Clear responsibility, easy to understand data flow
- **Maintainability:** Components don't depend on each other's internals
