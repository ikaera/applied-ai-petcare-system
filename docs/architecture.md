# System Architecture

## Table of Contents

- [Overview](#overview)
- [Full-Stack Layers](#full-stack-layers)
- [System Architecture Diagram](#system-architecture-diagram)
- [Components](#components)
- [Data Flow](#data-flow)
- [Design Principles](#design-principles)
- [Key Files](#key-files)
- [Why This Architecture?](#why-this-architecture)

---

## Overview

PawPal+ combines a scheduling engine with AI features. The system is modular: each component is independent and testable.

---

## Full-Stack Layers

**Presentation Layer**
- React UI (http://localhost:3000)
  - Task Manager component
  - Recommendation Engine component
  - A/B Comparison component
  - Responsive CSS styling

**API Layer**
- Flask REST API (http://localhost:5000)
  - 7 endpoints (health, pets, tasks, recommend, compare, plan)
  - CORS enabled for React
  - JSON request/response

**Application Layer**
- Python AI system (integrator, retriever, validator, planner)
- Scheduler logic (task management, conflict detection)
- Knowledge base (15 pet care documents)

**Data Layer**
- In-memory storage (can extend to database)
- knowledge_base.json (static documents)
- .env configuration (API keys)

### System Architecture Diagram

```mermaid
graph TB
    subgraph "Presentation"
        UI["React UI<br/>(Task Manager, Recommendations, A/B Test)"]
    end
    
    subgraph "API"
        API["Flask REST API<br/>(7 endpoints)"]
    end
    
    subgraph "Application Layer"
        SCHED["Scheduler<br/>(Task Mgmt, Conflicts)"]
        INTEGRATOR["AI Integrator<br/>(Orchestrator)"]
        
        subgraph "AI Components"
            RETRIEVER["RAG Retriever<br/>(Heuristic + Groq)"]
            VALIDATOR["Validator<br/>(5 Rules + Bias)"]
            PLANNER["Agentic Planner<br/>(6-Step Reasoning)"]
        end
    end
    
    subgraph "Data Layer"
        KB["Knowledge Base<br/>(15 Documents)"]
        CONFIG[".env Config<br/>(API Keys)"]
    end
    
    UI -->|axios| API
    API -->|calls| SCHED
    API -->|calls| INTEGRATOR
    
    SCHED -->|generates plan| INTEGRATOR
    INTEGRATOR -->|fetches docs| RETRIEVER
    INTEGRATOR -->|validates| VALIDATOR
    INTEGRATOR -->|reasons| PLANNER
    
    RETRIEVER -->|searches| KB
    RETRIEVER -->|reads key| CONFIG
    VALIDATOR -->|returns score| INTEGRATOR
    PLANNER -->|confidence| INTEGRATOR
    
    INTEGRATOR -->|enhanced plan| API
    API -->|JSON| UI
    
    style UI fill:#667eea,stroke:#333,color:#fff
    style API fill:#764ba2,stroke:#333,color:#fff
    style SCHED fill:#4CAF50,stroke:#333,color:#fff
    style INTEGRATOR fill:#FF9800,stroke:#333,color:#fff
    style KB fill:#2196F3,stroke:#333,color:#fff
```

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

**React → Flask → Python AI**
```
User Input (React UI)
    ↓
HTTP Request (axios)
    ↓
Flask API (flask_api.py)
    ├─→ Parse JSON
    ├─→ Route to handler
    └─→ Call Python system
    ↓
Python AI Processing
    ├─→ Scheduler (generate base plan)
    ├─→ AI Integrator
    │   ├─→ RAG Retriever (fetch knowledge)
    │   ├─→ Validator (check safety)
    │   └─→ Metrics (track quality)
    ↓
Response Data (JSON)
    ↓
HTTP Response
    ↓
React UI (display results)
```

**Command-Line (Direct Python)**
```
Python Script (main.py, agentic_demo.py)
    ↓
Scheduler (generate plan)
    ↓
AI Integrator (enhance with RAG + validation)
    ↓
Output (console, file, or JSON)
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

**Backend/API**
| File | Purpose |
|------|---------|
| `flask_api.py` | Flask REST API server with 7 endpoints |
| `pawpal_system.py` | Original scheduler (Owner, Pet, Task, Scheduler) |
| `src/ai/retriever.py` | RAG knowledge base search |
| `src/ai/validator.py` | Safety checks + bias detection |
| `src/ai/agentic_planner.py` | Multi-step reasoning with logging |
| `src/ai/integrator.py` | Component orchestration |
| `knowledge_base.json` | 15 curated pet care documents |

**Frontend**
| File | Purpose |
|------|---------|
| `frontend/src/App.js` | Main React component (tab navigation) |
| `frontend/src/components/TaskManager.js` | Task scheduling UI |
| `frontend/src/components/RecommendationEngine.js` | Single recommendation UI |
| `frontend/src/components/ABComparison.js` | A/B test comparison UI |
| `frontend/package.json` | React dependencies |

**Testing**
| File | Purpose |
|------|---------|
| `tests/test_ai_system.py` | AI component tests (22 tests) |
| `tests/test_groq_integration.py` | Dual-mode retrieval tests (11 tests) |
| `tests/test_pawpal.py` | Scheduler tests (47 tests) |
| `tests/test_agentic_planner.py` | Reasoning pipeline tests (3 tests) |

---

## Why This Architecture?

- **Modularity:** Can use scheduler alone, or add AI features incrementally
- **Testing:** Each component tested independently + end-to-end
- **Reliability:** Validation + confidence scores + guardrails
- **Clarity:** Clear responsibility, easy to understand data flow
- **Maintainability:** Components don't depend on each other's internals
