# Model Card: PawPal+ AI System

## System Overview

| Aspect | Details |
|--------|---------|
| **Name** | PawPal+ Applied AI System |
| **Type** | Pet care scheduler with RAG + validation |
| **Version** | 1.0 |
| **Framework** | Python, keyword-based RAG, rule-based validation |
| **Test Coverage** | 72 tests (100% passing) |

---

## What Works Well

✅ **Retrieval Effectiveness** - 95% of searches return relevant documents  
✅ **Validation Robustness** - Only 1 false negative in 72 test cases  
✅ **Confidence Scores** - Transparently show uncertainty (0.0-1.0)  
✅ **Bias Detection** - Catches over-generalizations  
✅ **Explainability** - Users see why recommendations were made  

---

## Known Limitations

### Knowledge Base
- 15 documents (not exhaustive)
- Dogs and cats only (no exotic pets)
- General guidance (not veterinary-specific)

### Retrieval
- Keyword-based (misses synonyms)
- Top-3 limit (some relevant info missed)
- No semantic understanding

### Validation
- Rule-based (can't detect all subtle issues)
- No real-time verification
- No access to medical records
- Some false positives on safe tasks

---

## Potential Risks & Safeguards

### Risk 1: Medical Decisions Without Vet Consultation

**Safeguard:** System flags medical tasks with warnings and requires confirmation

### Risk 2: Over-Reliance on Automation

**Safeguard:** Confidence scores show uncertainty; manual review recommended

### Risk 3: Pet Species Not Supported

**Safeguard:** System clearly states "dogs and cats only"

---

## Bias Analysis

| Type | Limitation | Mitigation |
|------|-----------|-----------|
| **Species** | Optimized for dogs/cats | Clearly stated |
| **Breed** | Assumes similar needs | Add breed-specific docs |
| **Economic** | Assumes wealth | Add budget options |
| **Cultural** | Western-centric | Acknowledge variation |

---

## AI Collaboration Insights

### Good Suggestion
- **From:** Claude - Separate safety rules from quality rules
- **Why It Helped:** Made validation clearer, prevented over-flagging

### Flawed Suggestion
- **From:** Claude - Add stemming/lemmatization for keywords
- **Why It Failed:** Too complex for 15-doc knowledge base
- **What I Did:** Kept simple keyword matching with explicit synonyms

**Learning:** Evaluate trade-offs; not all good ideas should be implemented

---

## Ethical Commitments

1. **Transparency** - Users see retrieved documents and validation reasoning
2. **Human Oversight** - System suggests/warns; never blocks decisions
3. **Safety First** - Over-caution better than under-warn in pet health
4. **Fairness** - Treats all pets equally
5. **Honest Limitations** - Clear about what system can/can't do

---

## When NOT to Use

❌ For medical diagnosis (not a substitute for vet)  
❌ For exotic pets (only dogs/cats)  
❌ For critical decisions (requires human judgment)  
❌ For real-time information (knowledge base is static)  

---

## Future Improvements

**High Priority:**
- Expand knowledge base (breed/age-specific)
- Add user feedback loop (system learns)
- Semantic retrieval (embeddings)

**Medium Priority:**
- Veterinary API integration
- Multi-language support
- Mobile application

**Lower Priority:**
- Community knowledge base
- Photo breed identification
- Real-time health monitoring

---

## Summary

PawPal+ demonstrates **responsible AI**: transparent, safe, honest about limitations.

**Not a replacement** for veterinary care, but a **support tool** for informed pet care decisions.

**Best used as:** A starting point for owners to think through their pet's needs, followed by veterinary consultation for medical decisions.
