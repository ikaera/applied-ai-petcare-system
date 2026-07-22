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