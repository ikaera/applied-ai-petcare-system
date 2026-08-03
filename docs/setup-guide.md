
`docs/setup-guide.md`

How can another developer install and run this project?

# Setup Guide

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Clone the Repository](#clone-the-repository)
- [Create Virtual Environment](#create-virtual-environment)
- [Install Dependencies](#install-dependencies)
- [Environment Configuration](#environment-configuration)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)


---

# Overview

This guide explains how to set up and run the `applied-ai-petcare-system` project locally.

The goal is to make the project reproducible so another developer can install, run, and test the system without additional configuration.


---

# System Requirements

## Required Software

Install:

- Python 3.11 or higher
- Git
- Code editor (recommended: Visual Studio Code)


## Verify Installation

Check Python:

```bash
python --version
````

Expected:

```text
Python 3.11+
```

Check Git:

```bash
git --version
```

---

# Clone the Repository

Clone the project:

```bash
git clone https://github.com/username/applied-ai-petcare-system.git
```

Move into the project folder:

```bash
cd applied-ai-petcare-system
```

---

# Create Virtual Environment

A virtual environment keeps project dependencies isolated.

## Windows

Create environment:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

## macOS/Linux

Create environment:

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

After activation, the terminal should show:

```text
(.venv)
```

---

# Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install project packages:

```bash
pip install -r requirements.txt
```

Verify installed packages:

```bash
pip list
```

---

# Environment Configuration

Some AI features may require external services.

Create an environment file:

```text
.env
```

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

## Important Notes

* Never commit `.env` files to GitHub.
* Add `.env` to `.gitignore`.
* Keep API keys private.

Example `.gitignore`:

```text
.env
.venv/
__pycache__/
logs/
```

---

# Project Structure

After setup, the project should look like:

```text
applied-ai-petcare-system/

├── README.md

├── docs/

├── diagrams/

├── src/

│   ├── app.py
│   ├── main.py
│   ├── petcare_system.py
│   └── ai/

├── data/

│   └── knowledge_base/

├── logs/

├── evaluations/

├── tests/

├── requirements.txt

└── .env
```

---

# Running the Application

## Run Command-Line Version

```bash
python -m src.main
```

Expected behavior:

* Loads sample data
* Generates a pet-care plan
* Displays scheduling results

---

## Run Streamlit Application

Start the web interface:

```bash
streamlit run src/app.py
```

The application will open in a browser.

---

# Running Tests

Run the complete test suite:

```bash
pytest
```

Run with detailed output:

```bash
pytest -v
```

Expected output:

```text
All tests passed
```

---

# AI Feature Testing

If AI components are enabled, verify:

## Retrieval

Check:

* Documents load correctly
* Relevant information is retrieved
* Responses use retrieved information

## Validation

Check:

* Invalid answers are detected
* Missing information is handled
* Unsafe outputs are flagged

## Reliability Evaluation

Check:

* Confidence scores are generated
* Evaluation results are saved
* Logs are created

---

# Troubleshooting

## Problem: Python command not found

Solution:

Install Python and make sure it is added to PATH.

Verify:

```bash
python --version
```

---

## Problem: Dependency installation fails

Try:

```bash
python -m pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

---

## Problem: Virtual environment is not activated

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

---

## Problem: Tests fail

Check:

1. Virtual environment is active
2. Dependencies are installed
3. Correct Python version is used

Run:

```bash
python --version

pip list

pytest -v
```

---

# Development Recommendations

For development:

1. Create a new branch:

```bash
git checkout -b feature-name
```

2. Make changes.

3. Run tests:

```bash
pytest
```

4. Commit changes:

```bash
git add .

git commit -m "Add feature"
```

5. Push changes:

```bash
git push origin feature-name
```

---

# Next Steps

After completing setup:

1. Review the architecture:

[Architecture Documentation](architecture.md)

2. Review the AI roadmap:

[Extensions Roadmap](extensions-roadmap.md)

3. Run the test suite:

[Testing Documentation](testing.md)


---

# Navigation

- [Back to README](../README.md)
- [Back to Top](#table-of-contents)
