
testing → How it is validated

`docs/testing.md`

How do we know the system works and is reliable?

# Testing and Reliability Evaluation

## Table of Contents

- [Overview](#overview)
- [Testing Goals](#testing-goals)
- [Testing Strategy](#testing-strategy)
- [Automated Testing](#automated-testing)
- [Unit Testing](#unit-testing)
- [AI Feature Testing](#ai-feature-testing)
- [Reliability Evaluation](#reliability-evaluation)
- [Guardrail Testing](#guardrail-testing)
- [Human Evaluation](#human-evaluation)
- [Example Test Results](#example-test-results)
- [Running Tests](#running-tests)
- [Future Testing Improvements](#future-testing-improvements)
- [Navigation](#navigation)


---

# Overview

This document explains how the `applied-ai-petcare-system` is tested and evaluated.

The goal is not only to verify that the software runs, but also to measure whether the AI system is:

- Accurate
- Reliable
- Safe
- Explainable
- Consistent


AI systems can produce incorrect or incomplete answers.

For this reason, testing is an important part of the design.


---

# Testing Goals

The testing strategy focuses on five areas:

## 1. Functional Correctness

Verify that the application works as expected.

Examples:

- Pets can be created
- Tasks can be added
- Schedules are generated correctly
- Data is saved and loaded


## 2. AI Behavior

Verify that AI features are properly integrated.

Examples:

- Retrieval improves answers
- AI uses provided context
- Recommendations follow system rules


## 3. Reliability

Measure how often the system produces useful results.

Examples:

- Confidence scores
- Validation results
- Error frequency


## 4. Safety

Prevent unsafe AI recommendations.

Examples:

- Missing medical context
- Unsupported claims
- Incorrect assumptions


## 5. Reproducibility

Another developer should be able to:

- Install the project
- Run tests
- Verify results


---

# Testing Strategy

The project uses multiple testing levels.

```

Testing Pyramid

```
    AI Evaluation Tests

          ▲

    Integration Tests

          ▲

    Unit Tests

          ▲

 Code Quality Checks
```

```


Testing layers:

| Testing Type | Purpose |
|---|---|
| Unit tests | Verify individual functions |
| Integration tests | Verify components work together |
| AI evaluation tests | Measure AI quality |
| Reliability tests | Measure confidence and failures |
| Human review | Evaluate usefulness |


---

# Automated Testing

Automated tests verify that the application continues working after changes.


The project uses:

- `pytest`
- Test datasets
- Evaluation scripts


Example structure:

```

tests/

├── test_petcare_system.py

├── test_scheduler.py

├── test_ai_retrieval.py

└── test_validation.py

````


---

# Unit Testing

Unit tests verify individual components.

Examples:

## Scheduler Tests

Test:

- Task ordering
- Priority selection
- Time limits
- Conflict detection


Example:

```python
def test_high_priority_task_selected_first():
    plan = scheduler.generate_plan(tasks)

    assert plan[0].priority == "high"
````

---

## Data Persistence Tests

Verify:

* Save works
* Load works
* Data remains unchanged

Example:

```python
def test_save_and_reload_owner():

    save_owner()

    loaded_owner = load_owner()

    assert loaded_owner.name == original.name
```

---

# AI Feature Testing

AI components require additional testing.

Traditional software tests:

```
Input → Expected Output
```

AI testing:

```
Input → Expected Behavior
```

Because AI outputs can vary, evaluation focuses on quality.

---

## Retrieval Testing

Verify:

* Correct documents are retrieved
* Relevant information is included
* Irrelevant information is minimized

Example:

| Query                | Expected Retrieved Topic | Result |
| -------------------- | ------------------------ | ------ |
| Dog feeding schedule | Nutrition documents      | Pass   |
| Grooming frequency   | Grooming documents       | Pass   |

---

## Validation Testing

Verify that unsafe answers are detected.

Example:

Input:

```
My dog has symptoms. Should I give medication?
```

Expected:

```
Request more information.
Recommend veterinary guidance.
```

Result:

```
Pass
```

---

# Reliability Evaluation

Reliability measures how trustworthy the AI output is.

The system evaluates:

## Confidence Score

Example:

```
Confidence Score: 0.85
```

Possible factors:

* Retrieved information quality
* Validation result
* Completeness of response

---

## Response Quality

Evaluate:

* Accuracy
* Relevance
* Explanation quality
* Safety

Example:

| Metric              | Score |
| ------------------- | ----: |
| Retrieval accuracy  |   90% |
| Validation success  |   95% |
| Explanation quality |   85% |

---

# Guardrail Testing

Guardrails prevent unsafe behavior.

The system checks:

## Missing Information

Example:

User:

```
My pet needs medicine.
```

System response:

```
Please provide:

- Medication name
- Pet age
- Pet weight
- Veterinary instructions
```

Expected:

Pass

---

## Unsupported Claims

The system should avoid:

```
This treatment will definitely cure your pet.
```

Preferred:

```
This information may help, but consult a veterinarian for diagnosis.
```

---

# Human Evaluation

Human review helps measure usefulness.

Evaluation should be recorded in a structured format.

Example:

| Test Input                  | Evaluation Criteria    | Result |
| --------------------------- | ---------------------- | ------ |
| Create daily pet plan       | Logical schedule       | Pass   |
| Ask unclear health question | Requests clarification | Pass   |
| Missing task information    | Handles gracefully     | Pass   |

---

# Example Test Results

Example final evaluation:

## Automated Tests

```
pytest

32 passed
```

## AI Evaluation

| Test                                 | Result |
| ------------------------------------ | ------ |
| Retrieval returns relevant documents | Pass   |
| AI uses retrieved context            | Pass   |
| Unsafe recommendation detection      | Pass   |
| Missing information handling         | Pass   |

## Reliability Summary

Example:

```
Average confidence score: 0.86

Validation success rate: 92%

Failed cases:
- Missing pet health information
- Ambiguous user questions
```

---

# Running Tests

From the project root:

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest
```

Run with detailed output:

```bash
pytest -v
```

Run AI evaluation tests:

```bash
python tests/run_evaluation.py
```

---

# Future Testing Improvements

Possible improvements:

## Larger Evaluation Dataset

Add:

* More user scenarios
* More pet-care examples
* Edge cases

## Automated Benchmarking

Create:

* Accuracy reports
* Performance dashboards
* Regression testing

## Continuous Testing

Integrate:

* GitHub Actions
* Automated test runs
* Deployment checks

## Human Feedback Loop

Collect:

* User ratings
* Corrections
* Improvement suggestions

---

# Navigation

* [Back to README](../README.md)
* [Back to Top](#table-of-contents)

