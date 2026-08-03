# PawPal+ Applied AI System

**An intelligent pet care task scheduler with retrieval-augmented generation and automated validation.**

## Table of Contents

- [Overview](#overview)
- [Original Project Summary](#original-project-summary)
- [AI Enhancements Implemented](#ai-enhancements-implemented)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Running the Application](#running-the-application)
- [Testing & Evaluation](#testing--evaluation)
- [Example Interactions](#example-interactions)
- [Design Decisions](#design-decisions)
- [Documentation](#documentation)

---

## Overview

**PawPal+** extends the original pet care scheduling system with a complete **RAG + Validation AI layer**. The system intelligently schedules pet care tasks while retrieving relevant knowledge from a curated knowledge base and validating all recommendations for safety and completeness.

**Key Value:** Provides pet owners with trustworthy, knowledge-backed task recommendations that include confidence scoring and safety validation.

---

## Original Project Summary

**Original Name:** PawPal+ (Pet Care Task Scheduler)

**Original Capabilities:**
- Multi-pet task management and organization
- Priority-based task scheduling (high, medium, low)
- Time-budgeted daily planning (fit tasks into available time)
- Recurring task support (daily, weekly)
- Scheduling conflict detection
- JSON-based data persistence
- Streamlit web interface
- Automated test suite

The original system solved the problem of organizing multiple pets' care needs into realistic daily plans within time constraints.

---

## AI Enhancements Implemented

### 1. **Retrieval-Augmented Generation (RAG)**

**What it does:**
- Searches a knowledge base of 15 pet care documents before making recommendations
- Retrieves relevant information about feeding, exercise, medications, health, and grooming
- Supports both dogs and cats with species-specific guidance

**Implementation:**
- `PetCareRetriever` class: keyword-based document search (TF-IDF style)
- Knowledge base: `knowledge_base.json` with 15 curated pet care documents
- Retrieval triggered for each scheduled task (retrieve by species + category)
- Top-3 most relevant documents retrieved per task

**Example:**
```
Task: "Morning walk for Mochi (dog)"
Retrieved Documents:
  1. Dog Health Basics (relevance: 50%)
  2. Dog Exercise Requirements (relevance: 50%)
```

### 2. **Recommendation Validator (Guardrails)**

**What it does:**
- Checks each recommendation for safety, completeness, and appropriateness
- Flags medical recommendations without supporting documentation
- Validates species-specific appropriateness (different rules for dogs vs. cats)
- Ensures recommendations match task category

**Implementation:**
- `RecommendationValidator` class: 4 validation rules
- Confidence scoring (0.0–1.0)
- Generates improvement suggestions when issues found
- Tracks validation issues: missing context, unsafe recommendations, insufficient info

**Example:**
```
Recommendation: "Give medication"
Issues Found: 
  - Missing context (no supporting docs)
  - Insufficient detail
Confidence: 0.7
Suggestion: "Add reference to supporting pet care documentation"
```

### 3. **AI System Integrator**

**What it does:**
- Orchestrates RAG retriever and validator into the scheduling workflow
- Enriches each planned task with retrieval results and validation
- Tracks system reliability metrics

**Key Features:**
- Seamless integration with existing Scheduler
- Metrics tracking (validation rate, confidence scores, retrieval quality)
- Interaction logging for debugging and evaluation

---

---

## Features

### Core Scheduling
- Multi-pet task management
- Priority-based scheduling (high → medium → low)
- Time-budget enforcement (fit tasks into available minutes)
- Recurring task support (daily, weekly)
- Conflict detection (two tasks at same time)

### AI-Enhanced Features
- **RAG Retrieval:** Searches knowledge base for relevant pet care information
- **Validation:** Checks recommendations for safety and completeness
- **Confidence Scoring:** Measures reliability of each recommendation (0.0–1.0)
- **Guardrails:** Prevents unsafe medical recommendations without vet context
- **Species-Aware:** Different rules for dogs vs. cats
- **Metrics Tracking:** Measures system reliability and retrieval quality

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Input (Owner, Pets, Tasks)              │
└─────────────────────────────────────┬───────────────────────────┘
                                      │
                    ┌─────────────────▼────────────────┐
                    │  Scheduling Engine               │
                    │  (Priority sort, Time budget)    │
                    └─────────────────┬────────────────┘
                                      │
                    ┌─────────────────▼──────────────────────┐
                    │  AI Integrator (Orchestrator)         │
                    │  ├─ RAG Retriever                     │
                    │  │  └─ Knowledge Base (15 docs)       │
                    │  └─ Recommendation Validator          │
                    │     └─ Validation Rules & Guardrails  │
                    └─────────────────┬──────────────────────┘
                                      │
                    ┌─────────────────▼──────────────────────┐
                    │  Enhanced Plan                         │
                    │  (with Retrieval & Validation Results) │
                    └─────────────────┬──────────────────────┘
                                      │
                    ┌─────────────────▼──────────────────────┐
                    │  Output                                │
                    │  ├─ Console Display                    │
                    │  ├─ Streamlit UI                       │
                    │  └─ Metrics & Logging                  │
                    └────────────────────────────────────────┘
```

See detailed diagram: [architecture.mmd](diagrams/architecture.mmd)

---

## Project Structure

```
applied-ai-petcare-system/
├── README.md (this file)
├── requirements.txt
├── knowledge_base.json (15 pet care documents)
├── pawpal_system.py (original scheduling logic)
├── main.py (demo with RAG + validation)
├── app.py (Streamlit UI)
├── formatting.py (display utilities)
│
├── src/
│   └── ai/
│       ├── __init__.py
│       ├── retriever.py (RAG retriever)
│       ├── validator.py (recommendation validator)
│       └── integrator.py (AI system orchestrator)
│
├── tests/
│   ├── test_pawpal.py (original system tests)
│   └── test_ai_system.py (RAG + validation tests)
│
├── diagrams/
│   └── architecture.mmd (system architecture)
│
├── docs/
│   ├── architecture.md
│   ├── extensions-roadmap.md
│   ├── testing.md
│   ├── setup-guide.md
│   ├── model_card.md
│   └── workflow.md
│
└── assets/ (for diagrams/screenshots)
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/username/applied-ai-petcare-system.git
cd applied-ai-petcare-system
```

### 2. Create a Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Command-Line Demo (with RAG + Validation)

```bash
python main.py
```

**Output includes:**
- Daily schedule table with retrieval & validation status
- Detailed task recommendations with retrieved documents
- System reliability metrics

### Streamlit Web Interface

```bash
streamlit run app.py
```

---

## Testing & Evaluation

### Run All Tests

```bash
pytest tests/ -v
```

### Test Results Summary

**Total Tests:** 18  
**Status:** ✅ All Passing  

**Test Coverage:**

| Component | Tests | Status |
|-----------|-------|--------|
| RAG Retriever | 6 | ✅ All Pass |
| Validator | 6 | ✅ All Pass |
| AI Integrator | 5 | ✅ All Pass |
| End-to-End | 1 | ✅ All Pass |

**Key Test Cases:**
- ✅ Retriever loads 15 documents
- ✅ Retriever finds dog-specific information
- ✅ Retriever finds cat-specific information
- ✅ Validator flags medical recommendations without docs
- ✅ Validator accepts safe recommendations
- ✅ Integrator enhances full plans with retrieval & validation
- ✅ Metrics correctly track system performance

### Reliability Metrics

From a 4-pet, 8-task sample plan:

```
Total items evaluated: 8
Items validated: 8
Valid recommendations: 6/8 (75%)
Average confidence score: 0.84
Average retrieval quality: 0.68
Validation success rate: 75%
```

---

## Example Interactions

### Example 1: Dog Task Scheduling

**Input:**
```
Owner: Jordan | Available time: 90 minutes
Pets: Mochi (dog) - 4 tasks | Whiskers (cat) - 4 tasks
```

**System Output (Partial):**
```
✅ Morning Walk (30m)
   Pet: Mochi | Category: walk | Priority: HIGH
   📚 Retrieved: Dog Exercise Requirements (90% relevance)
   ✓ Validation: PASS (confidence: 1.0)
   
⚠️ Evening Meds (5m)
   Pet: Mochi | Category: meds | Priority: HIGH
   📚 Retrieved: Dog Medications (50% relevance)
   ⚠️ Validation: REVIEW (confidence: 0.85)
   Suggestion: Ensure recommendation aligns with task type
```

### Example 2: Retrieval in Action

**Task:** "Feed breakfast" for dog Mochi

**Retrieval Results:**
1. **Dog Feeding Guide** (100% relevance) - "Adult dogs typically need 1-2 meals per day. Food portions depend on dog size, age, and activity level."
2. **Dog Health Basics** (50% relevance) - "Dogs require daily exercise and proper nutrition..."

**Validation:** ✓ PASS - confidence 0.85

---

## Design Decisions

### 1. Rule-Based Validation Over ML Models

**Decision:** Use hand-crafted validation rules instead of training a classifier.

**Why:**
- **Transparency:** Every validation decision can be explained
- **Safety:** Control over what gets flagged as unsafe
- **Speed:** No model training required
- **Reliability:** Fewer failure modes in production

**Trade-off:** Less flexible than ML but more trustworthy for critical pet health decisions.

### 2. Keyword-Based Retrieval Over Vector Embeddings

**Decision:** Use TF-IDF style keyword matching for RAG.

**Why:**
- **No dependencies:** Works without external APIs or embeddings
- **Fast:** Instant results on small knowledge base
- **Interpretable:** Users can see why documents were retrieved
- **Maintainable:** Easy to update knowledge base

**Trade-off:** Less semantic understanding than embeddings, but sufficient for structured pet care categories.

### 3. Modular AI Layer

**Decision:** Separate AI components (retriever, validator, integrator) from core scheduling logic.

**Why:**
- **Testability:** Each component tested independently
- **Replaceability:** Can swap out components (e.g., upgrade to embeddings later)
- **Maintainability:** Core scheduling logic unchanged
- **Scalability:** Easy to add new AI components

### 4. Knowledge Base as Static JSON

**Decision:** Curate a fixed knowledge base rather than querying external APIs.

**Why:**
- **Control:** Only trusted information in knowledge base
- **Consistency:** Same results every time
- **Privacy:** No external API calls
- **Cost:** No per-query fees

**Trade-off:** Manual updates needed to add new information.

---

---

## Documentation

| Document | Purpose |
|----------|---------|
| [Architecture Details](docs/architecture.md) | System design, components, data flow |
| [Setup Guide](docs/setup-guide.md) | Installation and configuration steps |
| [Testing Strategy](docs/testing.md) | Test coverage and evaluation methodology |
| [AI Extensions Roadmap](docs/extensions-roadmap.md) | Future AI features and enhancements |
| [Workflow](docs/workflow.md) | Development process and milestones |
| [Model Card](docs/model_card.md) | **Responsible AI reflection** (limitations, bias, ethics) |

---

## Future Improvements

### Stretch Features
- **RAG Enhancement:** Add custom document chunking, vector embeddings, multi-source retrieval
- **Agentic Workflow:** Implement multi-step reasoning loops with Claude API
- **Fine-Tuning:** Train specialized model for pet care task understanding
- **Test Harness:** Build automated evaluation script with predefined test cases

### Performance Improvements
- Vector embeddings for semantic retrieval (vs. keyword matching)
- LLM-powered validation (vs. rule-based)
- Caching for frequently requested documents
- Multi-threaded retrieval for large knowledge bases

### Feature Additions
- User feedback learning loop (improve validation over time)
- Integration with veterinary APIs (real-time health alerts)
- Multi-language support
- Mobile app version

---

## License

This project is for educational and portfolio purposes.

---

## Contributing

Found a bug or have a suggestion? Please open an issue or submit a pull request.

---

## Acknowledgments

- Original PawPal+ scheduling logic and design
- CodePath AI110 course framework and requirements
- Pet care expertise and knowledge base curation

---

## Navigation

- [Back to Top](#table-of-contents)
- [View Architecture Diagram](diagrams/architecture.mmd)
- [Responsible AI Model Card](docs/model_card.md)