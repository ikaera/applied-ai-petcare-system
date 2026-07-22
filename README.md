
`README.md → How to use`

What is this project and how do I run it quickly?

# applied-ai-petcare-system

## Table of Contents

- [Overview](#overview)
- [Original Project](#original-project)
- [AI Enhancements](#ai-enhancements)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Example Usage](#example-usage)
- [Documentation](#documentation)
- [Future Improvements](#future-improvements)


---

# Overview

`applied-ai-petcare-system` is an AI-enhanced pet care planning application.

The system helps pet owners organize daily care tasks, create schedules, and receive AI-assisted recommendations.

The project combines:

- Python software engineering
- Scheduling algorithms
- Streamlit user interface
- Retrieval-Augmented Generation (RAG)
- AI validation and reliability evaluation


The goal is to build a reliable AI assistant that helps users make better pet-care decisions while providing clear explanations.

---

# Original Project

This project extends the previous `petcare-system` application.

The original system was designed to help pet owners manage multiple pets and organize care tasks.

Original capabilities included:

- Creating pets and tasks
- Tracking task completion
- Priority-based scheduling
- Time-budgeted daily planning
- Recurring tasks
- Conflict detection
- Data persistence
- Streamlit user interface
- Automated testing


The applied AI version improves the original system by adding intelligent retrieval, planning, and evaluation features.

---

# AI Enhancements

The project adds AI components to improve decision-making and reliability.

Current and planned AI capabilities:

- Retrieval-Augmented Generation (RAG)
  - Retrieves trusted pet-care information before generating answers.

- AI planning assistance
  - Helps create task plans based on user goals and constraints.

- Response validation
  - Checks AI outputs for missing information and unsafe recommendations.

- Reliability scoring
  - Measures confidence and quality of AI-generated responses.

More details:

[AI Extension Roadmap](docs/extensions-roadmap.md)

---

# Features

## Core Application Features

- Manage pets and care tasks
- Create daily schedules
- Prioritize important activities
- Detect scheduling conflicts
- Support recurring tasks
- Store and reload user data


## AI Features

- Retrieve information from pet-care documents
- Generate explanations for recommendations
- Validate AI responses
- Evaluate system reliability
- Record system decisions and errors


---

# Project Structure

```text
applied-ai-petcare-system/

├── README.md

├── docs/
│   ├── workflow.md
│   ├── setup-guide.md
│   ├── architecture.md
│   ├── extensions-roadmap.md
│   ├── testing.md
│   └── model_card.md

├── diagrams/
│   └── architecture.mmd

├── src/
│   ├── app.py
│   ├── main.py
│   ├── petcare_system.py
│   └── ai/

├── tests/

└── requirements.txt
````

---

# Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/username/applied-ai-petcare-system.git

cd applied-ai-petcare-system
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For more detailed setup instructions:

[Setup Guide](docs/setup-guide.md)

---

# Running the Application

## Run the Python application

```bash
python -m src.main
```

## Run the Streamlit interface

```bash
streamlit run src/app.py
```

---

# Testing

Run all tests:

```bash
pytest
```

The test suite covers:

* Core scheduling logic
* Task management
* AI components
* Validation rules
* Reliability checks

Detailed testing information:

[Testing Documentation](docs/testing.md)

---

# Example Usage

## User Input

```
I have 30 minutes today.
My dog needs exercise and medication.
Create a care plan.
```

## System Output

```
Recommended plan:

1. Give medication
   Reason:
   - High priority
   - Health-related task

2. Complete short walk
   Reason:
   - Fits remaining time
   - Supports daily exercise

Confidence score:
0.87
```

---

# Documentation

Detailed project documentation:

| Document                                         | Description                             |
| ------------------------------------------------ | --------------------------------------- |
| [Workflow](docs/workflow.md)                     | Six-step development workflow           |
| [Setup Guide](docs/setup-guide.md)               | Detailed installation and configuration |
| [Architecture](docs/architecture.md)             | System design and data flow             |
| [Extensions Roadmap](docs/extensions-roadmap.md) | AI feature development plan             |
| [Testing](docs/testing.md)                       | Testing strategy and evaluation         |
| [Model Card](docs/model_card.md)                 | Responsible AI documentation            |

---

# Future Improvements

Possible future enhancements:

* Add more pet-care knowledge sources
* Improve retrieval accuracy
* Add advanced agent-based planning
* Improve reliability scoring
* Add user feedback learning loop
* Expand evaluation datasets

---

# License

This project is for educational and portfolio purposes.


# Navigation

- [Back to Top](#table-of-contents)