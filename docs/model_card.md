model_card → How it is responsible


`docs/model_card.md`

How should this AI system be used safely and responsibly?

# Model Card: Applied AI Pet Care System

## Table of Contents

- [Overview](#overview)
- [System Description](#system-description)
- [Purpose and Intended Use](#purpose-and-intended-use)
- [Target Users](#target-users)
- [AI Components](#ai-components)
- [Data Sources](#data-sources)
- [How the System Works](#how-the-system-works)
- [Responsible AI Considerations](#responsible-ai-considerations)
- [Safety Guardrails](#safety-guardrails)
- [Known Limitations](#known-limitations)
- [Potential Risks](#potential-risks)
- [Evaluation Summary](#evaluation-summary)
- [AI Collaboration Reflection](#ai-collaboration-reflection)
- [Future Improvements](#future-improvements)
- [Navigation](#navigation)


---

# Overview

This model card documents the design, intended use, limitations, and responsible AI considerations of the `applied-ai-petcare-system`.

The project extends the original `petcare-system` application by adding AI capabilities including:

- Retrieval-Augmented Generation (RAG)
- AI-assisted planning
- Response validation
- Reliability evaluation


The purpose of this document is to clearly explain what the system does and how it should be used responsibly.


---

# System Description

The `applied-ai-petcare-system` is an AI-enhanced pet-care planning application.

The system helps users:

- Organize pet-care activities
- Create daily schedules
- Receive AI-assisted recommendations
- Understand why recommendations were generated


The system combines:

- Python application logic
- Scheduling algorithms
- Streamlit interface
- AI components
- Testing and evaluation tools


---

# Purpose and Intended Use

## Intended Purpose

The system is designed to assist pet owners with:

- Planning daily care tasks
- Organizing routines
- Understanding general pet-care information
- Improving consistency of care activities


Examples:

- Feeding reminders
- Exercise planning
- Grooming schedules
- Task prioritization


---

## Appropriate Use

The system should be used as:

- A planning assistant
- An educational tool
- A productivity aid


It should not replace:

- Veterinarian advice
- Professional medical diagnosis
- Emergency care decisions


---

# Target Users

The primary users are:

- Pet owners
- Pet-care planners
- Developers studying applied AI systems


The system is designed for users who want:

- Better organization
- More explainable recommendations
- AI-assisted planning


---

# AI Components

## Retrieval-Augmented Generation (RAG)

Purpose:

Retrieve relevant pet-care information before generating responses.


Benefits:

- Reduces unsupported answers
- Provides additional context
- Improves transparency


---

## Agentic Planning

Purpose:

Allow AI to perform multi-step planning.


Example workflow:

```

User Goal

↓

Analyze Tasks

↓

Create Plan

↓

Check Constraints

↓

Return Recommendation

```


---

## Validation System

Purpose:

Review AI output before showing it to users.


Checks:

- Missing information
- Unsafe recommendations
- Unsupported statements


---

## Reliability Evaluation

Purpose:

Measure confidence and system performance.


Examples:

- Confidence scores
- Test results
- Validation outcomes


---

# Data Sources

The system may use:


## Application Data

Examples:

- User-created pets
- Tasks
- Scheduling information


## Knowledge Sources

Examples:

- Pet-care documents
- General educational resources


The system should document external sources used for AI retrieval.


---

# How the System Works

High-level workflow:


```

User Input

↓

Application Processing

↓

AI Retrieval

↓

AI Generation

↓

Validation

↓

Reliability Evaluation

↓

Final Response

```


Each stage improves reliability before presenting information to the user.


---

# Responsible AI Considerations

## Transparency

The system should explain:

- Why a recommendation was generated
- What information influenced the result
- What limitations exist


---

## Human Oversight

Users remain responsible for final decisions.

The AI provides assistance, not professional judgment.


---

## Avoiding Overconfidence

The system should avoid presenting uncertain information as fact.


Example:


Avoid:

```

This treatment will solve the problem.

```


Prefer:

```

This information may help, but professional advice may be needed.

```


---

# Safety Guardrails

The system includes safeguards such as:


## Requesting More Information

If information is incomplete:

Example:

```

More details are needed before making a recommendation.

```


Possible missing information:

- Pet age
- Breed
- Symptoms
- Previous conditions


---

## Avoiding Medical Diagnosis

The system should:

- Provide general information
- Encourage professional consultation when needed


It should not:

- Diagnose diseases
- Prescribe medication
- Replace veterinary professionals


---

## Validation Before Output

AI responses should be checked for:

- Accuracy
- Completeness
- Safety


---

# Known Limitations

The system has several limitations.


## AI Accuracy

AI responses may still contain mistakes.

Retrieval and validation reduce errors but do not eliminate them.


---

## Knowledge Coverage

The quality of recommendations depends on:

- Available documents
- Retrieval quality
- Data freshness


---

## User Input Quality

Incorrect or incomplete user information can affect results.


Example:

Missing:

- Pet age
- Health information
- Task details


may produce less useful recommendations.


---

## Not a Medical System

The system is not designed for:

- Emergency situations
- Diagnosis
- Treatment decisions


---

# Potential Risks

## Incorrect Recommendations

Risk:

AI may provide incomplete information.


Mitigation:

- Retrieval
- Validation
- User warnings


---

## User Over-Reliance

Risk:

Users may trust AI output too much.


Mitigation:

- Explain limitations
- Encourage professional guidance


---

## Data Quality Issues

Risk:

Poor knowledge sources may affect responses.


Mitigation:

- Review sources
- Update documents
- Evaluate outputs


---

# Evaluation Summary

The system is evaluated using:


## Automated Tests

Examples:

- Scheduler tests
- Data persistence tests
- AI module tests


Example:

```

pytest

All tests passed

```


---

## AI Evaluation

Metrics:

| Metric | Purpose |
|---|---|
| Retrieval relevance | Measures document quality |
| Validation success | Measures safety checks |
| Confidence score | Measures reliability |
| Response quality | Measures usefulness |


---

## Human Review

Human evaluation checks:

- Is the response understandable?
- Is the recommendation useful?
- Are limitations clear?


---

# AI Collaboration Reflection

## How AI Was Used

AI tools were used as:

- Coding assistants
- Documentation helpers
- Design discussion partners
- Debugging assistants


The final implementation decisions were reviewed and tested by the developer.


---

## Helpful AI Suggestion

Example:

AI suggested:

```

Separate AI functionality into independent modules.

```


Why it helped:

- Improved maintainability
- Made testing easier
- Reduced complexity


---

## Flawed AI Suggestion

Example:

AI suggested:

```

Use AI-generated answers without additional validation.

```


Why it was rejected:

- AI responses can be incorrect
- Reliability requires testing and guardrails


---

## Lessons Learned

Important lessons:

- AI systems require evaluation, not only implementation.
- Good architecture improves AI reliability.
- Human judgment remains important.
- Documentation is part of engineering quality.


---

# Future Improvements

Future improvements may include:

- Larger evaluation datasets
- More advanced retrieval systems
- Better confidence calibration
- User feedback integration
- Production monitoring


---

# Navigation

- [Back to README](../README.md)
- [Back to Top](#table-of-contents)
```

Your documentation set is now complete:

```text
docs/

├── workflow.md              ✅
├── setup-guide.md           ✅
├── architecture.md          ✅
├── extensions-roadmap.md    ✅
├── testing.md               ✅
└── model_card.md            ✅
```

Your `README.md` can now stay short and professional, while these files contain the detailed engineering documentation.

---

# Navigation

- [Back to README](../README.md)
- [Back to Top](#table-of-contents)