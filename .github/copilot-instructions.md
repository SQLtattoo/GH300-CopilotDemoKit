# Project Conventions — GitHub Copilot Demo Kit

These instructions define the coding conventions for this project.
GitHub Copilot should follow these when generating suggestions.

## Naming Conventions

- Use `snake_case` for all functions, variables, and module names.
- Use `PascalCase` for classes and dataclasses.
- Prefix private helpers with a single underscore: `_helper_function()`.
- Constants are `UPPER_SNAKE_CASE` and defined at module top.

## Error Handling

- Never use bare `except:` — always catch specific exceptions.
- Raise `ValueError` for invalid input, `RuntimeError` for operational failures.
- All error messages must be human-readable sentences starting with a capital letter.
- Log errors at `logger.error()` level before raising.

## Logging

- Use the shared logger from `src/logger.py` — never use `print()`.
- Import as: `from src.logger import get_logger` then `logger = get_logger(__name__)`.
- Log at INFO for normal operations, WARNING for recoverable issues, ERROR for failures.
- Include context in log messages: `f"Failed to load employee {emp_id}: {error}"`.

## Type Hints

- All public functions must have type hints on parameters and return types.
- Use `Optional[T]` for nullable values, not `T | None`.
- Use `List`, `Dict`, `Tuple` from `typing` (Python 3.9 compat).

## Testing

- One test file per source module: `test_<module>.py`.
- Use pytest fixtures from `conftest.py` — no test-local setup.
- Test class names: `Test<FunctionName>` (e.g., `TestValidateSalary`).
- Each test function tests exactly one behavior.
- Target 90%+ coverage.

## Documentation

- All public functions must have Google-style docstrings.
- Docstrings describe WHAT the function does, not HOW.
- Include `Args:`, `Returns:`, and `Raises:` sections where applicable.

## Data Handling

- Employee data is stored as JSON in a flat file.
- All file I/O goes through `src/storage.py` — no direct file access in other modules.
- Validate all external input before processing.
