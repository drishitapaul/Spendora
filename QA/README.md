# Spendora — QA & Test Automation

**[🌐 Live Demo](https://spendora-cyan.vercel.app/)**

A QA and test automation suite developed for **Spendora**, a web-based finance tracking application. The project demonstrates manual testing practices alongside automated API and UI testing.

## Testing Coverage

* Functional and regression testing
* Positive and negative test scenarios
* REST API testing
* UI test automation
* Input validation and error handling
* Test execution and reporting

## Automation

* **Python**
* **Pytest**
* **Selenium WebDriver**
* **Requests**

## Application Stack

* React.js
* Flask
* SQLite
* REST APIs

## Test Suite

**10 automated tests**

* 7 API tests
* 3 UI tests

The suite validates API responses, transaction creation and validation, application loading, form behaviour, and critical transaction workflows.

## QA Documentation

* `TEST_PLAN.md` — Testing scope, approach and coverage
* `TEST_CASES.md` — Functional and negative test scenarios
* `BUG_REPORT.md` — Defect reporting template
* `test-report.html` — Automated test execution report

## Running Tests

```bash
pip install selenium pytest pytest-html requests
pytest automation/test_spendora.py -v
```

Generate an HTML report:

```bash
pytest automation/test_spendora.py -v --html=QA/test-report.html --self-contained-html
```
