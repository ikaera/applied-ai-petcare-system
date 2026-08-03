# PawPal+ Demo Day Presentation

**5-7 minute engineer's pitch + Q&A**

---

## Part 1: The Problem (1 minute)

### Opening
"Pet owners with multiple pets face a real problem: How do I organize my dog's walk, medication, and feeding, plus my cat's grooming and feeding—all within 90 minutes? And how do I make sure those recommendations are safe and fair?"

### Why It Matters
- **Safety:** Medical mistakes can hurt animals
- **Fairness:** Pets need personalized advice, not generic "all dogs need..." rules
- **Trust:** Pet owners need to understand why the system makes recommendations

### The Scenario
- Owner: Jordan, available time: 90 minutes
- Pets: Mochi (golden retriever) and Whiskers (domestic cat)
- Tasks: Morning walk, feedings, grooming, medication, playtime
- **Challenge:** Fit everything in safely and fairly

---

## Part 2: The Logic (2-3 minutes)

### The 4-Component AI System

**1. RAG Retrieval** (Knowledge-backed)
- Searches 15 curated pet care documents before recommending
- Example: "Morning walk for Mochi" → retrieves "Dog Exercise Requirements" + "Dog Health Basics"

**2. Validation Guardrails** (Safety)
- Medical tasks require veterinary documentation
- Tasks must be species-appropriate
- Confidence scores show when system is uncertain

**3. Agentic Planning** (Transparent Reasoning)
- 6-step decision pipeline: constraints → priorities → conflicts → optimization → validation → execution
- Each step has confidence tracking
- Overall plan viability score

**4. Bias Detection** (Fairness)
- Flags over-generalizations ("All dogs need...")
- Ensures individual pet context considered
- Suggests personalized improvements

### Live Example
```
Input: "Evening meds" for Mochi (no vet docs)
RAG: Retrieved 2 documents on dog medication
Validation: ⚠ REVIEW (0.70 confidence)
Issue: Missing veterinary documentation
Suggestion: Add vet context before proceeding
```

---

## Part 3: The Reliability (1-2 minutes)

### How We Know It Works

**Testing:**
- 69 automated tests (100% passing)
- All components tested independently + end-to-end

**Guardrails in Action:**

| Scenario | Result | Confidence |
|----------|--------|-----------|
| Medical without vet docs | ⚠ REVIEW | 0.70 |
| Safe feeding task | ✓ PASS | 1.00 |
| Biased recommendation | ⚠ BIASED | 0.80 |
| Personalized recommendation | ✓ PASS | 1.00 |

**Metrics from Real Run:**
- 8 tasks evaluated
- 6/8 pass validation (75%)
- Average confidence: 0.84
- 100% test pass rate

---

## Part 4: The Reflection (1-2 minutes)

### What Surprised Me
1. **Simplicity wins:** Keyword-based retrieval works better than embeddings for structured pet care tasks
2. **Transparency matters:** Users trust rule-based validation more than black-box ML classifiers
3. **Testing is essential:** Guardrails only matter if thoroughly tested

### Design Choices (and Trade-offs)
- **Keyword retrieval** (not embeddings) → Simpler, interpretable, sufficient for pet care
- **Rule-based validation** (not ML) → Transparent, safe for medical decisions
- **Fixed 6-step planning** (not dynamic agents) → More debuggable, matches problem scope
- **Static knowledge base** (not APIs) → Controlled information, no privacy concerns

### What I'd Do Differently
1. Add vector embeddings later (semantic understanding)
2. Implement user feedback loop (system learns from corrections)
3. Integrate with real veterinary APIs
4. Dynamic agentic planning (not fixed steps)

### Key Learnings
- **Responsible AI first:** Transparency and safety > raw accuracy
- **Systems thinking:** AI is integration, testing, monitoring—not just models
- **User-centric design:** Build for real pet owners, not just impressive demos
- **Effective collaboration:** Use AI for good ideas, but maintain critical judgment

---

## Quick Links

- **GitHub:** https://github.com/ikaera/applied-ai-petcare-system
- **Full Documentation:** [README.md](README.md)
- **Technical Details:** [docs/architecture.md](docs/architecture.md)
- **How to Run:** [README.md → Installation](README.md#installation)

---

## Q&A Tips

**"How does RAG work with such a small knowledge base?"**
→ It's sufficient for structured pet care tasks with clear keywords. Embeddings would be overkill.

**"Why not use an LLM instead of rules?"**
→ For safety-critical decisions (pet health), transparent rules beat black-box predictions.

**"What's the biggest limitation?"**
→ Static knowledge base. Future versions would integrate real veterinary APIs.

**"How confident are you in the system?"**
→ For non-medical tasks: very confident (0.95+). For medical: properly cautious (0.70), requiring vet confirmation.

