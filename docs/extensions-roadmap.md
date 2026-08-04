# Future Roadmap

## Current State

✅ RAG retrieval (keyword-based)  
✅ Validation guardrails (5 rules + bias detection)  
✅ Agentic planning (6-step reasoning)  
✅ 83 automated tests (100% passing)  
✅ Modular architecture  

---

## Short Term (1-2 weeks)

**User Feedback Loop**
- Store user corrections to recommendations
- Learn from corrections (improve future suggestions)
- Track which recommendations users override

**Expanded Knowledge Base**
- Add more pet care documents (expand from 15)
- Add breed-specific guidelines
- Add age-specific care recommendations

**Caching & Performance**
- Cache frequently retrieved documents
- Speed up multi-pet schedules
- Batch processing for bulk imports

---

## Medium Term (1-2 months)

**Semantic Retrieval**
- Replace keyword search with embeddings
- Better synonym handling
- Semantic similarity (not just keywords)

**LLM-Powered Validation**
- Use Claude/GPT alongside rule-based validation
- Detect novel safety issues
- More nuanced fairness checking

**Dynamic Agentic Planning**
- Replace fixed 6-step pipeline with dynamic steps
- Self-correcting (agent revises its own decisions)
- Tool calling for external information

---

## Long Term (3+ months)

**Veterinary Integration**
- Real-time API to veterinary databases
- Breed-specific health guidelines
- Drug interaction checking

**Multi-Language Support**
- Translate knowledge base
- Support multiple languages in UI
- Localized pet care guidelines

**Mobile Application**
- IOS/Android app
- Push notifications for scheduled tasks
- Photo identification of pet breed

**Community Knowledge Base**
- User-contributed pet care tips
- Voting/ranking system
- Moderation pipeline

---

## Why These Improvements?

| Feature | Benefit | Effort |
|---------|---------|--------|
| Feedback loop | System learns, improves over time | Medium |
| Embeddings | Better semantic understanding | Medium |
| LLM validation | Catch novel issues | Medium |
| Veterinary APIs | Real-time accurate information | High |
| Mobile app | Reach more users | High |

---

## Architecture Ready For:

✅ **Swappable components** - Can replace keyword retriever with embeddings  
✅ **Optional logging** - Can enable file logging when needed  
✅ **Dependency injection** - Can inject custom validators or planners  
✅ **Extensible rules** - Can add new validation rules without refactoring  

---

## Trade-offs

**Current approach:**
- Simple (no external APIs, embeddings, or complex ML)
- Explainable (users see exactly why decisions were made)
- Tested (83 tests, 100% passing)
- Reliable (rule-based, no model failures)

**Future enhancements will:**
- Add complexity (embeddings, LLMs, APIs)
- Require more sophisticated testing
- May reduce explainability (black-box models)
- Gain accuracy but lose some control

**Recommendation:** Start with current approach, add features incrementally based on real user feedback.
