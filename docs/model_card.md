# Model Card: PawPal+ Applied AI System

## System Overview

Name: PawPal+ Applied AI System
Type: Pet care task scheduling with RAG + validation
Version: 1.0 (Applied AI Extension)
Date: August 2, 2026
Framework: Python, keyword-based RAG, rule-based validation

---

## System Limitations

### Knowledge Base Limitations

1. Coverage Gaps
   - Knowledge base contains 15 documents (not exhaustive)
   - Covers general dog and cat care
   - No information on exotic pets

2. Retrieval Limitations
   - Keyword-based search misses synonyms
   - Top-3 limit means some relevant information is missed

### Validation Limitations

1. Rule-Based Checks
   - Cannot detect all subtle unsafe recommendations
   - Over-cautions on some safe tasks

2. No Real-Time Verification
   - Cannot check veterinary availability
   - No access to pet medical records

---

## Potential Misuses & Safeguards

### Misuse 1: Medical Decisions Without Vet Consultation

Risk: User treats AI recommendations as medical advice.

Safeguards:
- Validation flags medical tasks with warnings
- Knowledge base emphasizes veterinary consultation
- System requires confirmation for medical tasks

### Misuse 2: Over-Reliance on Automation

Risk: User schedules without considering individual pet needs.

Safeguards:
- Confidence scores show uncertainty levels
- Validation issues explained with suggestions
- Manual review recommended

---

## Bias Analysis

### Species Bias
- System optimized for dogs and cats only
- Mitigation: Clearly state supported species

### Breed Bias
- Assumes all dogs have similar needs
- Mitigation: Add breed-specific information

### Economic Bias
- Recommends professional services (assumes wealth)
- Mitigation: Add budget-friendly alternatives

### Cultural Bias
- Assumes Western pet care norms
- Mitigation: Acknowledge cultural variation

---

## Testing & Surprising Findings

### What Worked Well

- Retrieval Effectiveness: 95% of searches returned relevant documents
- Validation Robustness: Only 1 false negative in 18 test cases
- User Experience: Color-coded output made results clear

### What Was Surprising

- Confidence Variability: Ranged 0.7-1.0 for similar tasks
- False Positives: Some safe tasks flagged as risky
- Retrieval Trade-offs: More documents = more noise in some cases

### What Didn't Work

- Exact Phrase Matching: Missed synonyms
- Negation Handling: Could not distinguish "CAN eat" vs "CANNOT eat"

---

## Responsible AI Reflection

### Helpful Suggestion from AI

Context: Asked how to structure validation rules.

Suggestion: "Separate safety rules (medical) from quality rules (completeness)."

Why It Helped:
- Made validation logic clearer
- Improved user experience
- Prevented over-flagging

### Flawed Suggestion from AI

Context: Asked how to improve retrieval without embeddings.

Suggestion: "Add stemming and lemmatization."

Why It Was Flawed:
- Too complex for 15-document knowledge base
- Introduced false positives
- Time not justified by results

What I Did Instead: Kept simple keyword matching with explicit synonyms.

Learning: Evaluate trade-offs; not all good ideas should be implemented.

---

## Ethical Commitments

1. Transparency: Users see retrieved documents and validation reasoning
2. Human Oversight: System suggests/warns; never blocks decisions
3. Safety First: Over-caution better than under-warn in pet health
4. Fairness: Treats all pets equally

---

## Future Work

1. Expand knowledge base (breed/age/condition-specific documents)
2. Implement vector embeddings for semantic retrieval
3. Add user customization
4. Create feedback loop for validation improvement
5. Partner with veterinarians
6. Multi-language support
7. External security audit

---

## Conclusion

PawPal+ demonstrates responsible AI: transparent, safe, honest about limitations.
Not a replacement for veterinary care, but a support tool for informed decisions.
