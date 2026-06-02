"""Input validation for employee data."""

import re
import os
from typing import List, Tuple

from src.logger import get_logger

logger = get_logger(__name__)

VALID_DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]
MIN_SALARY = 30000.0
MAX_SALARY = 500000.0


# --- Chat - Fix Demo ---
def validate_employee_name(name: str) -> Tuple[bool, str]:
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters"
    if len(name) > 50:
        return False, "Name must not exceed 50 characters"
    pattern = r"^[A-Za-z\s\-']+"
    if not re.match(pattern, name):
        return False, "Name contains invalid characters"
    return True, ""


def validate_salary(salary) -> Tuple[bool, str]:
    try:
        salary = float(salary)
    except (TypeError, ValueError):
        return False, "Salary must be a number"
    if salary < MIN_SALARY:
        return False, f"Salary must be at least {MIN_SALARY:,.2f}"
    if salary > MAX_SALARY:
        return False, f"Salary must not exceed {MAX_SALARY:,.2f}"
    return True, ""


def validate_department(department: str) -> Tuple[bool, str]:
    if department not in VALID_DEPARTMENTS:
        return False, f"Invalid department. Must be one of: {', '.join(VALID_DEPARTMENTS)}"
    return True, ""


# --- Chat - Doc Demo ---
def validate_employee_data(data: dict) -> Tuple[bool, List]:
    errors = []

    name_valid, name_err = validate_employee_name(data.get("first_name", ""))
    if not name_valid:
        errors.append(f"first_name: {name_err}")

    name_valid, name_err = validate_employee_name(data.get("last_name", ""))
    if not name_valid:
        errors.append(f"last_name: {name_err}")

    salary_valid, salary_err = validate_salary(data.get("salary"))
    if not salary_valid:
        errors.append(f"salary: {salary_err}")

    dept_valid, dept_err = validate_department(data.get("department", ""))
    if not dept_valid:
        errors.append(f"department: {dept_err}")

    if errors:
        return False, errors
    return True, []


# --- Code Completion Demo ---
def validate_date_string(date_str: str) -> Tuple[bool, str]:
    """Validate that a string is a valid ISO date format (YYYY-MM-DD)."""
    if not date_str or not isinstance(date_str, str):
        return False, "Date is required"
    # Copilot should complete the validation logic
