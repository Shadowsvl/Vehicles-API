# Project Constitution

This document defines the non-negotiable principles, rules, and standards for the Vehicles API project. All contributors must adhere to these guidelines to ensure consistency, maintainability, and quality.

## 1. Coding Standards

### Style & Formatting
- **PEP 8**: All Python code must strictly follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- **Formatter**: Use `Black` or `Ruff` for automatic formatting.
- **Linting**: No linting errors are permitted.

### Typing
- **Static Typing**: All function signatures (arguments and return values) must use type hints.
- **Syntax**: Use modern Python 3.11+ type hinting syntax (e.g., `list[str]` instead of `List[str]`).

### Documentation
- **Docstrings**: All public modules, classes, and functions must have docstrings following the **Google Style**.
- **Clarity**: Comments should explain *why*, not *what* (the code should explain *what*).

## 2. Architecture Principles

### API Design
- **RESTful**: Adhere to REST maturity level 2 (Resources, HTTP Verbs).
- **Versioning**: All endpoints must be versioned (e.g., `/api/v1/...`).
- **Statelessness**: The API must be stateless.

### Separation of Concerns
- **Layered Architecture**:
    - **API Layer** (FastAPI Routers): Handling HTTP requests/responses.
    - **Service Layer**: Core business logic and rules.
    - **Data Access Layer** (Repositories): Database interactions.
- **Dependency Injection**: Use FastAPI's dependency injection system to manage dependencies.

## 3. Testing Requirements

### Approach
- **TDD**: Test-Driven Development is mandatory. Write the test *before* the implementation.
- **Isolation**: Unit tests should be isolated and fast. Use mocks for external dependencies (database, external APIs).

### Coverage
- **Threshold**: Minimum **90%** code coverage is required for all new code.
- **Tools**: Use `pytest` for running tests and `pytest-cov` for coverage reports.

## 4. Error Handling Patterns

### Response Format
All errors must return a consistent JSON structure:

```json
{
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human-readable error description.",
    "details": {
      "field_name": "Specific validation error"
    }
  }
}
```

### HTTP Status Codes
- **400 Bad Request**: Validation errors, malformed requests.
- **401 Unauthorized**: Authentication failure.
- **403 Forbidden**: Permission denied.
- **404 Not Found**: Resource not found.
- **409 Conflict**: Resource state conflict.
- **500 Internal Server Error**: Unexpected server errors (do not expose stack traces to client).

## 5. Commit Strategy

### Format
Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat: ...` for new features.
- `fix: ...` for bug fixes.
- `docs: ...` for documentation purposes.
- `refactor: ...` for code refactoring.
- `test: ...` for adding/modifying tests.
- `chore: ...` for maintenance tasks.

### Message Structure
```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Granularity
- **Atomic Commits**: Each commit should do one thing and do it well.
- **Task-Based**: Commits should map to specific tasks or tickets.
