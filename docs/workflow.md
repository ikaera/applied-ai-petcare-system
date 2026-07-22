
`workflow → How it was built`

How was this project planned, built, and improved?

# Six-Step Development Workflow

## Table of Contents

- [Overview](#overview)
- [Workflow Goals](#workflow-goals)
- [Step 1: Understand Requirements and Define the Problem](#step-1-understand-requirements-and-define-the-problem)
- [Step 2: Design System Architecture](#step-2-design-system-architecture)
- [Step 3: Implement Core Application Logic](#step-3-implement-core-application-logic)
- [Step 4: Integrate AI Components](#step-4-integrate-ai-components)
- [Step 5: Test, Evaluate, and Improve Reliability](#step-5-test-evaluate-and-improve-reliability)
- [Step 6: Document, Present, and Prepare Portfolio](#step-6-document-present-and-prepare-portfolio)
- [Recommended Development Timeline](#recommended-development-timeline)
- [Git Development Workflow](#git-development-workflow)
- [Final Project Checklist](#final-project-checklist)
- [Navigation](#navigation)


---

# Overview

This document describes the six-step workflow used to develop the `applied-ai-petcare-system`.

The purpose of this workflow is to transform a previous software project into a complete applied AI system.

The process focuses on:

- Good software engineering practices
- Modular AI integration
- Reliable evaluation
- Clear documentation
- Professional presentation


The workflow should be followed from initial planning through final portfolio delivery.


---

# Workflow Goals

By following this workflow, the project should achieve:

- A working AI-enabled application
- Clean system architecture
- Reproducible setup process
- Tested AI behavior
- Documented design decisions
- Portfolio-ready presentation


The workflow separates development into clear stages so problems can be discovered early.


---

# Step 1: Understand Requirements and Define the Problem

## Goal

Understand the original project and identify how AI can improve it.


## Tasks

Review the original `petcare-system` project.

Identify:

- Current features
- Current limitations
- User problems
- Opportunities for AI integration


Example:


Original system:

```

Pet task scheduler

```


Possible AI improvement:

```

AI assistant that retrieves pet-care information
and explains scheduling decisions.

```


---

## Questions to Answer

Before coding, define:

- Who is the user?
- What problem does the system solve?
- Why is AI useful?
- What limitations exist?


---

## Expected Output

Create:

- Project description
- AI enhancement plan
- Feature requirements


Example:

```

Problem:
Pet owners need help organizing care tasks.

AI Improvement:
Use RAG to provide reliable pet-care recommendations.

```


---

# Step 2: Design System Architecture

## Goal

Create a clear design before implementation.


## Tasks

Design:

- System components
- Data flow
- AI modules
- Testing strategy


Create:

```

diagrams/architecture.mmd

```


The diagram should show:

```

Input

↓

Application Logic

↓

AI Components

↓

Validation

↓

Output

```


---

## Architecture Questions

Define:

- Where does AI run?
- What data does AI use?
- How are results validated?
- How are errors handled?


---

## Expected Output

Files:

```

docs/architecture.md

diagrams/architecture.mmd

```


---

# Step 3: Implement Core Application Logic

## Goal

Build a stable software foundation before adding AI.


## Tasks

Improve existing application:


Examples:

- Clean class structure
- Improve error handling
- Add reusable functions
- Add tests


The core system should work without AI.


Example:

```

Pet

↓

Task

↓

Scheduler

↓

Daily Plan

```


---

## Development Principles

Follow:

- Small changes
- Frequent testing
- Clear naming
- Modular code


Avoid:

- Large untested changes
- Mixing AI code with business logic


---

## Expected Output

Working application:

```

src/

├── app.py

├── main.py

└── petcare_system.py

```


---

# Step 4: Integrate AI Components

## Goal

Add AI features that improve system behavior.


AI should be integrated into the workflow.

It should not be a separate demo script.


---

## Possible AI Features


### Retrieval-Augmented Generation (RAG)

Add:

- Knowledge base
- Retriever
- Context-aware responses


Flow:

```

Question

↓

Retriever

↓

Relevant Information

↓

AI Response

```


---

### Agentic Workflow

Add:

- Planning
- Tool usage
- Error recovery


Flow:

```

Goal

↓

Plan

↓

Execute

↓

Validate

↓

Improve

```


---

### Reliability Features

Add:

- Confidence scores
- Validation
- Logging


---

## Expected Output

Example structure:

```

src/

└── ai/

```
├── retriever.py

├── planner.py

├── validator.py

└── evaluator.py
```

```


---

# Step 5: Test, Evaluate, and Improve Reliability

## Goal

Prove that the system works.


AI systems require more than successful execution.

They need evaluation.


---

## Tasks


Test:


### Software Behavior

Examples:

- Unit tests
- Integration tests


### AI Behavior

Examples:

- Retrieval quality
- Response accuracy
- Safety checks


### Reliability

Examples:

- Confidence scoring
- Error handling
- Logging


---

## Document Results


Include:

- Test commands
- Test outputs
- Evaluation tables
- Known limitations


Example:


| Test | Result |
|---|---|
| Scheduler works | Pass |
| Retrieval finds relevant data | Pass |
| Unsafe output detected | Pass |


---

## Expected Output

Files:

```

docs/testing.md

test results

```


---

# Step 6: Document, Present, and Prepare Portfolio

## Goal

Make the project understandable to others.


A strong engineering project is not only code.

It also includes:

- Documentation
- Explanation
- Demonstration


---

## Documentation Tasks


Complete:


```

README.md

docs/

├── workflow.md

├── setup-guide.md

├── architecture.md

├── testing.md

├── extensions-roadmap.md

└── model_card.md

````


---

## Presentation Tasks


Prepare:

- 5-7 minute presentation
- Demo workflow
- Architecture explanation
- Testing results
- Lessons learned


---

## Portfolio Requirements


Include:

- GitHub repository
- Project summary
- Screenshots or examples
- AI engineering reflection


---

# Recommended Development Timeline

## Phase 1: Planning

Duration:

1 day


Complete:

- Requirements
- Architecture
- Roadmap


---

## Phase 2: Core Development

Duration:

2-3 days


Complete:

- Refactoring
- Core functionality
- Testing foundation


---

## Phase 3: AI Integration

Duration:

3-5 days


Complete:

- RAG
- Validation
- AI workflow


---

## Phase 4: Evaluation

Duration:

1-2 days


Complete:

- Testing
- Reliability metrics
- Documentation


---

## Phase 5: Presentation

Duration:

1 day


Complete:

- Demo
- Portfolio updates


---

# Git Development Workflow

Recommended workflow:


## Create Feature Branches


Example:

```bash
git checkout -b feature/rag-system
````

---

## Commit Small Changes

Example:

```bash
git add .

git commit -m "Add document retrieval module"
```

---

## Push Regularly

```bash
git push origin feature/rag-system
```

---

## Merge After Testing

Only merge features that:

* Pass tests
* Are documented
* Work correctly

---

# Final Project Checklist

## Setup

* [ ] Project installs successfully
* [ ] README setup instructions work
* [ ] Dependencies are documented

## Architecture

* [ ] Mermaid architecture diagram exists
* [ ] Components are explained

## AI Features

* [ ] AI feature is integrated
* [ ] AI affects system behavior
* [ ] Limitations are documented

## Testing

* [ ] Automated tests exist
* [ ] AI evaluation exists
* [ ] Results are documented

## Documentation

* [ ] README is clear
* [ ] Setup guide exists
* [ ] Model card is complete

## Presentation

* [ ] Demo prepared
* [ ] Portfolio description written

---

# Navigation

* [Back to README](../README.md)
* [Back to Top](#table-of-contents)
