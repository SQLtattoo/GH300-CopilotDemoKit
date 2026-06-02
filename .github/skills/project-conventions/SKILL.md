---
name: project-conventions
description: Coding standards and patterns enforced in this project. Invoked when generating or reviewing code to ensure consistency with team standards.
---

# Project Conventions Skill

## When This Skill Applies

Use this knowledge when:
- Generating new functions or classes
- Reviewing code for style compliance
- Deciding how to handle errors, logging, or naming
- Writing tests

## Naming

| Context | Convention | Example |
|---------|-----------|---------|
| Functions/variables | snake_case | `get_employee_by_id` |
| Classes | PascalCase | `Employee` |
| Constants | UPPER_SNAKE_CASE | `MAX_SALARY` |
| Private helpers | Leading underscore | `_parse_date` |
| Test classes | Test + FunctionName | `TestValidateSalary` |
| Test functions | test + behavior | `test_rejects_negative_salary` |

## Error Handling Pattern

```python
from src.logger import get_logger
logger = get_logger(__name__)

def risky_operation(data: dict) -> Result:
    try:
        # operation
        pass
    except ValueError as e:
        logger.error(f"Invalid input for operation: {e}")
        raise
    except OSError as e:
        logger.error(f"File operation failed: {e}")
        raise RuntimeError(f"Operation failed: {e}") from e
```

Rules:
- Never bare `except:`
- `ValueError` for bad input, `RuntimeError` for operational failures
- Log at ERROR before raising
- Human-readable messages starting with capital letter

## Logging Pattern

```python
from src.logger import get_logger
logger = get_logger(__name__)

# Levels:
logger.info(f"Loaded {count} employees from {filepath}")      # Normal operations
logger.warning(f"Invalid sort key '{key}', defaulting")       # Recoverable issues
logger.error(f"Failed to parse employee {emp_id}: {error}")   # Failures
```

- NEVER use `print()` — always use the shared logger
- Always include context (IDs, counts, file paths) in messages

## Type Hints

- All public functions: full type annotations on params and return
- Use `Optional[T]` not `T | None` (Python 3.9 compat)
- Import from `typing`: `List`, `Dict`, `Tuple`, `Optional`

## Testing Structure

```python
class TestFunctionName:
    def test_happy_path(self, fixture):
        # Arrange
        input_data = fixture

        # Act
        result = function_under_test(input_data)

        # Assert
        assert result == expected

    def test_edge_case(self):
        pass
```

- One assertion per test
- Use conftest.py fixtures exclusively
- Parametrize for input variations
