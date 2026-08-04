# Development Workflow

## Overview

This project was developed in 7 stages, starting from an existing pet care scheduler and adding AI capabilities, then building a modern web interface.

---

## Phase 1: Understand & Plan

**Goal:** Understand original system, identify AI opportunities

**Done:**
- Identified original PawPal+ scheduler (task management, time budgeting)
- Found gap: recommendations lack knowledge backing and safety validation
- Planned 4 AI features (RAG, validation, agentic planning, bias detection)

---

## Phase 2: Design Architecture

**Goal:** Create modular, testable system

**Key Decisions:**
- Separate scheduler from AI components (no tight coupling)
- Each component independent and testable
- Confidence scoring for transparency
- Rule-based validation (explainable, reliable)

**Result:** Clean architecture with clear data flow

---

## Phase 3: Implement Core AI

**Done:**
1. **RAG Retriever** - Keyword-based document search
2. **Validator** - 5 safety rules + bias detection
3. **Integrator** - Combines components
4. **Agentic Planner** - 6-step reasoning pipeline

**Key Challenge:** Making logging optional (no side effects during tests)

---

## Phase 4: Comprehensive Testing

**Coverage:**
- RAG tests (6) - document loading, retrieval accuracy
- Validator tests (13) - safety rules, bias detection, **combination tests**
- Integrator tests (5) - component interaction
- Scheduler tests (47) - original system still works
- **Total: 83 tests, 100% passing**

**Key Addition:** Combination tests verify multiple rules interact correctly

---

## Phase 5: Documentation & Simplification

**Original:** 7 redundant files (README, PROJECT_SUMMARY, GRADING_VERIFICATION, etc.)

**Simplified to:**
- README.md - Single source of truth
- PRESENTATION.md - Demo Day pitch (speaker notes)
- docs/ - Technical reference (not duplicating)
- ai_interactions.md - Implementation details
- reflection.md - Design thinking

**Result:** No maintenance burden, clear navigation

---

## Phase 6: Portfolio Preparation

**Final checks:**
- All tests passing ✓
- Code clean and modular ✓
- Documentation simple and clear ✓
- Logging side effects fixed ✓
- Combination tests added ✓
- Ready for grading and interviews ✓

---

## Phase 7: Full-Stack Web Interface

**Goal:** Build a modern interactive UI for better portfolio presentation

**Implemented:**
1. **Flask API** - 7 endpoints for task management and recommendations
2. **React Frontend** - 3 feature tabs (Task Manager, Recommendations, A/B Test)
3. **API Integration** - Axios calls from React to Flask backend
4. **Responsive Design** - Mobile-friendly CSS styling
5. **A/B Testing UI** - Compare retrieval modes side-by-side
6. **Deployment Guide** - Setup instructions for GitHub Pages + Render/Railway

**Key Technical Decisions:**
- Flask (simple, no frameworks needed)
- React hooks (no Redux complexity)
- REST API (clean, standard)
- Responsive CSS (no bootstrap dependency)
- CORS enabled (development-friendly)

**Result:** Portfolio-grade full-stack application showcasing both backend and frontend skills

---

## Key Learning

| Lesson | Why It Matters |
|--------|----------------|
| Test combinations, not just single cases | Catches subtle bugs in rule interactions |
| Dependency injection from the start | No side effects, code is testable |
| Single source of truth | Maintenance burden goes to zero |
| Measure twice, cut once | Design first, code second |

---

## Timeline

- **Week 1:** Architecture design + initial implementation
- **Week 2:** All AI components complete + basic tests
- **Week 3:** Comprehensive testing + logging refactor
- **Week 4:** Documentation cleanup + final polish
- **Week 5:** Flask API + React frontend development

**Total effort:** ~50 hours (design, code, test, document, full-stack)

---

## What Would Change?

If starting fresh, would:
1. ✅ Do this - Start with test design (not after)
2. ✅ Do this - Make logging optional from day 1
3. ✅ Do this - Write combination tests early
4. ❓ Maybe - Use embeddings instead of keywords (complexity vs. simplicity trade-off)
5. ❓ Maybe - Use LLM validation (less explainable but more powerful)

**Current approach:** Simple, testable, explainable. Good foundation for scaling.
