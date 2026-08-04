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
- 83 automated tests (100% passing)
- 11 new integration tests for dual-mode retrieval
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

## Live Demo Steps (5-7 minutes)

### Setup (1 minute)
```bash
# 1. Clone and setup
git clone https://github.com/ikaera/applied-ai-petcare-system.git
cd applied-ai-petcare-system

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify it works
pytest tests/ -q
# Result: 83 passed
```

### Demo 1: Basic System Run (2 minutes)
```bash
python main.py
```

**What you'll see:**
- DAILY SCHEDULE table showing:
  - Time, Pet name, Task description
  - Validation status (PASS/REVIEW)
  - Confidence score (0.0-1.0)
- RETRIEVED DOCUMENTS showing which knowledge was used
- SYSTEM METRICS showing reliability stats
- Example:
  ```
  Morning walk (Mochi, dog)
  Status: PASS (0.95 confidence)
  Retrieved: Dog Exercise Requirements, Dog Health Basics
  ```

### Demo 2: Agentic Reasoning (2 minutes)
```bash
python agentic_demo.py
```

**What you'll see:**
- 6-step reasoning trace:
  1. Analyze Constraints → confidence: 0.95
  2. Assess Priorities → confidence: 0.90
  3. Detect Conflicts → confidence: 0.70
  4. Optimize Schedule → confidence: 0.85
  5. Validate Plan → confidence: 0.90
  6. Execute Plan → confidence: 0.95
- Overall Plan Viability: 87.5% (VIABLE)
- Clear explanation of each decision

### Demo 3: Comparison & Testing (Optional)
```bash
# See both retrieval modes compared
python comparison_demo.py

# A/B test both modes
python ab_testing.py

# Run full test suite
pytest tests/ -v
```

---

## Portfolio: What This Project Says About Me

### Professional Reflection

I build AI systems that are **trustworthy, transparent, and genuinely useful**—not just technically impressive.

This project demonstrates six key principles:

**1. Responsible AI First**
Every recommendation includes confidence scores and validation results. The system explicitly warns when uncertain rather than silently failing. I prioritize transparency and safety over raw accuracy.

**2. Systems Thinking**
I understand that AI isn't just models—it's integration, testing, monitoring, and continuous improvement. This project includes RAG retrieval, rule-based validation, agentic reasoning, comprehensive testing (83 tests), and honest reflection on limitations.

**3. Practical Problem-Solving**
I chose keyword-based retrieval over embeddings (simpler, sufficient). Rule-based validation over ML classifiers (more trustworthy for pet health). No over-engineering; every design choice is justified and fits the problem scope.

**4. Attention to Users**
The system is designed for real pet owners, not just to impress reviewers. Output is clear and actionable. Confidence scores help users make informed decisions. Guardrails prevent dangerous medical advice without veterinary context.

**5. Quality & Reliability**
I write extensive tests (83/83 passing), document design decisions thoroughly, and reflect critically on limitations. The codebase is modular, maintainable, and extensible.

**6. Effective AI Collaboration**
I used AI effectively during development—asking for help with architecture, validation rules, and testing strategies. But I also recognized when AI suggestions were over-complicated and chose simpler alternatives that better fit the problem.

### Key Technical Achievements
- **RAG System:** 15-document knowledge base with species-specific retrieval
- **Validation Framework:** 5-rule safety engine + bias detection
- **Agentic Planning:** 6-step reasoning with confidence tracking
- **Test Coverage:** 83/83 passing (100%)
- **Dual-Mode Retrieval:** Heuristic + Groq API with seamless fallback

### What I Learned
- Simplicity often beats complexity (keyword retrieval > embeddings for this domain)
- Transparency builds trust more than accuracy alone
- Testing is foundational to reliable AI systems
- Good software engineering principles apply to AI just as much

---

## Portfolio Artifacts

### GitHub Repository
**Link:** https://github.com/ikaera/applied-ai-petcare-system
**Status:** Production-ready, fully tested
**Branch:** main (with 26 commits documenting the development process)

### Reproducible Execution Evidence
**All in README.md:**
- Installation: Step-by-step setup guide
- Quick Reference: Command cheat sheet
- Examples: 3+ complete worked scenarios
- Testing: 83/83 tests passing
- Output samples: Real terminal outputs in code blocks

### Optional Loom Video Walkthrough
A 5-7 minute walkthrough is encouraged for human reviewers but NOT required for grading. The text-based evidence in README.md is sufficient for automated grading.

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

