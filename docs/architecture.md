architecture → How it works

`docs/architecture.md`

How does the system work internally?

# System Architecture

## Table of Contents

- [Overview](#overview)
- [Architecture Goals](#architecture-goals)
- [High-Level Architecture](#high-level-architecture)
- [System Components](#system-components)
- [Data Flow](#data-flow)
- [AI Components](#ai-components)
- [Architecture Diagram](#architecture-diagram)
- [Design Decisions](#design-decisions)
- [Future Architecture Improvements](#future-architecture-improvements)


---

# Overview

This document describes the architecture of the `applied-ai-petcare-system`.

The system extends the original `petcare-system` application by adding AI capabilities while maintaining a clean separation between:

- User interface
- Business logic
- Scheduling engine
- AI services
- Evaluation and reliability components


The main design goal is to create a modular AI system that is:

- Easy to understand
- Easy to test
- Easy to extend
- Reliable and maintainable


---

# Architecture Goals

The architecture follows these principles:

## 1. Separation of Responsibilities

Each component should have one clear purpose.

Example:

- Scheduler handles task planning
- Retriever handles knowledge search
- Validator checks AI output
- Evaluator measures quality


## 2. Modular AI Integration

AI functionality should be independent from the core application.

The system should continue working even if AI services are unavailable.


## 3. Reliability First

AI output should not be accepted blindly.

The system includes:

- Validation
- Logging
- Testing
- Confidence scoring


## 4. Explainable Decisions

The system should explain:

- Why a task was selected
- Why information was retrieved
- Why a recommendation was generated


---

# High-Level Architecture

The system follows this architecture:

```

User
|
|
v
Streamlit Interface
|
|
v
Application Logic
|
+----------------+
|                |
v                v
Scheduler       AI Layer
|                |
|                |
v                |
Task Data         |
|
+---------+---------+
|                   |
v                   v
Retriever           Validator
|
v
Knowledge Base

```
    |
    v
```

Reliability Evaluator

```
    |
    v

  Final Response
```

```


---

# System Components

## 1. User Interface Layer

Location:

```

src/app.py

```


Purpose:

Provides interaction between the user and the system.


Responsibilities:

- Collect user input
- Display schedules
- Show AI recommendations
- Display validation results


Technology:

- Streamlit


---

# 2. Core Application Layer

Location:

```

src/petcare_system.py

```


Purpose:

Contains the main business logic.


Responsibilities:

- Manage pets
- Manage tasks
- Track completion
- Store application state


Core objects:

- Owner
- Pet
- Task
- Scheduler


---

# 3. Scheduling Engine

Purpose:

Creates optimized pet-care plans.


Responsibilities:

- Sort tasks
- Prioritize important activities
- Respect time limits
- Detect conflicts
- Generate daily plans


Example:

Input:

```

Available time: 60 minutes

```


Output:

```

1. Medication
2. Feeding
3. Walk

```


---

# 4. AI Layer

Location:

```

src/ai/

```


Purpose:

Provides intelligent assistance.


Possible modules:

```

ai/

├── retriever.py

├── planner.py

├── validator.py

└── evaluator.py

```


---

# AI Components

## Retrieval-Augmented Generation (RAG)

Purpose:

Improve responses by retrieving information from trusted sources.


Flow:

```

User Question

```
  |
  v
```

Retriever

```
  |
  v
```

Relevant Documents

```
  |
  v
```

AI Model

```
  |
  v
```

Final Answer

```


Example:

User:

```

My dog is refusing food.

```


System:

1. Searches pet-care knowledge documents
2. Retrieves relevant information
3. Generates recommendation
4. Validates response


---

## Agentic Planning

Purpose:

Allow AI to complete multi-step tasks.


Example:

User:

```

Create today's pet-care plan.

```


Agent workflow:

```

Understand Goal

```
  |
```

Analyze Tasks

```
  |
```

Create Plan

```
  |
```

Check Constraints

```
  |
```

Return Result

```


---

## Validation Layer

Purpose:

Check AI responses before showing them to users.


Validation checks:

- Missing information
- Unsafe recommendations
- Unsupported claims
- Low confidence responses


Example:

AI response:

```

Give medication immediately.

```


Validator:

```

Missing:

* Medication name
* Pet weight
* Veterinary guidance

Result:
Needs clarification

```


---

## Reliability Evaluation

Purpose:

Measure system performance.


Metrics:

- Retrieval quality
- Response confidence
- Validation success rate
- Test accuracy


Example:

```

Confidence Score: 0.87

Validation:
Passed

Retrieval:
3 relevant documents found

```


---

# Data Flow

The complete system flow:


```

1. User enters request

   ```
    |

    v
   ```

2. Application receives input

   ```
    |

    v
   ```

3. Scheduler analyzes tasks

   ```
    |

    v
   ```

4. AI layer retrieves information

   ```
    |

    v
   ```

5. AI generates recommendation

   ```
    |

    v
   ```

6. Validator checks output

   ```
    |

    v
   ```

7. Evaluator calculates reliability

   ```
    |

    v
   ```

8. User receives final response

```


---

# Architecture Diagram

The official architecture diagram is stored as:

```

diagrams/architecture.mmd

````


Mermaid source:

```mermaid
flowchart TD

    User[User]

    UI[Streamlit Interface]

    Core[Application Logic]

    Scheduler[Scheduling Engine]

    AI[AI Layer]

    Retriever[RAG Retriever]

    Knowledge[Knowledge Base]

    Validator[Response Validator]

    Evaluator[Reliability Evaluator]

    Output[Final Response]


    User --> UI

    UI --> Core

    Core --> Scheduler

    Core --> AI

    AI --> Retriever

    Retriever --> Knowledge

    AI --> Validator

    Validator --> Evaluator

    Evaluator --> Output

    Output --> UI
````

---

# Design Decisions

## Keep Core Logic Separate From AI

Decision:

AI features are placed in separate modules.

Reason:

* Easier testing
* Easier replacement of AI providers
* Better maintainability

---

## Use Retrieval Instead of AI-Only Answers

Decision:

Use external knowledge sources.

Reason:

AI models may generate incorrect information.

Retrieval improves:

* Accuracy
* Transparency
* Trust

---

## Add Validation Before User Output

Decision:

Never display AI output without checking.

Reason:

AI systems can produce:

* Incorrect answers
* Missing context
* Unsafe suggestions

---

## Store Logs and Evaluation Results

Decision:

Track system behavior.

Reason:

Helps:

* Debug problems
* Improve reliability
* Understand AI decisions

---

# Future Architecture Improvements

Possible future improvements:

## Multi-Agent Architecture

Add specialized agents:

* Scheduling agent
* Health information agent
* Safety agent

## Improved Knowledge Retrieval

Add:

* Vector database
* Multiple data sources
* Document ranking

## Advanced Evaluation

Add:

* Automated benchmarks
* User feedback scoring
* Continuous evaluation pipeline

## Production Deployment

Future deployment options:

* Cloud API
* Containerization
* Database storage
* Monitoring dashboard

```

Next file:

`docs/extensions-roadmap.md`  
(4 AI extension ideas with implementation roadmap, components, milestones, and expected outcomes).
```
---

# Navigation

- [Back to README](../README.md)
- [Back to Top](#table-of-contents)