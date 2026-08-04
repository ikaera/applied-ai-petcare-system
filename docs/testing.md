# Testing Strategy

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [What Tests Verify](#what-tests-verify)
- [Running Tests](#running-tests)
- [Key Test Cases](#key-test-cases)
- [Test Quality](#test-quality)
- [Future Improvements](#future-improvements)

---

## Overview

The project has **83 automated tests** (100% passing). Tests verify both functionality and AI behavior.

---

## Test Structure

### Component Tests (Unit)

| Component | Tests | Verifies |
|-----------|-------|----------|
| RAG Retriever | 6 | Loads documents, finds species-specific info, respects limits |
| Validator | 13 | Safety rules, bias detection, confidence scores |
| Integrator | 5 | Retrieval works, validation applied, metrics tracked |
| End-to-End | 1 | Full workflow (scheduling → RAG → validation) |
| Scheduler | 47 | Original system still works (task management, conflicts, etc.) |

**Total: 83 tests**

---

## What Tests Verify

### Correctness
- Retriever loads all 15 documents
- Validator detects medical tasks without vet docs
- Confidence scores stay within 0.0-1.0

### Rule Interactions
- Medical + biased simultaneously (both detected, confidence drops)
- Missing docs + biased (combined severity reflected)
- Safe tasks approved immediately

### Reliability
- Bias detection flags over-generalizations
- Individual pet context required
- Guardrails prevent unsafe recommendations

### Integration
- Components work together in main workflow
- Metrics calculated correctly
- No side effects (no unwanted log files)

---

## Running Tests

**All tests:**
```bash
pytest tests/ -v
```

**Specific component:**
```bash
pytest tests/test_ai_system.py::TestValidator -v
```

**Show coverage:**
```bash
pytest tests/ --cov=src
```

---

## Key Test Cases

**RAG Retrieval:**
- Finds dog-specific documents
- Finds cat-specific documents
- Respects top_k parameter

**Validation Safety:**
- Medical without docs → ⚠ REVIEW (0.70)
- Safe feeding → ✓ PASS (1.00)
- Biased recommendation → ⚠ BIASED (0.80)

**Bias Detection:**
- "All dogs need..." → flagged
- "Based on Mochi's age..." → accepted
- Combined issues detected correctly

**Integration:**
- Plan enhanced with retrieval + validation
- Metrics tracked accurately
- No test pollution (no log files created)

---

## Test Quality

**Precise Testing:**
- Not just "does it fail gracefully"
- But "do multiple rules interact correctly?"
- Combination tests ensure guardrails work together

**Clean Tests:**
- No side effects (logging is opt-in)
- Each test independent
- Easy to debug failures

---

## Future Improvements

- Add property-based tests (more edge cases)
- Test with different knowledge bases
- Load testing (how many tasks at scale?)
- Integration with real veterinary data
