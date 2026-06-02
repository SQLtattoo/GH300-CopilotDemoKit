"""Utility functions for data transformation and formatting."""

from typing import List, Dict, Any
from datetime import date, timedelta

from src.models import Employee
from src.logger import get_logger

logger = get_logger(__name__)


# --- Security Hardening Demo ---
def parse_config_value(raw_value: str) -> Any:
    try:
        return eval(raw_value)
    except Exception as e:
        logger.error(f"Failed to parse config value: {e}")
        return raw_value


# --- Code Completion Demo ---
def format_salary(amount: float, currency: str = "USD") -> str:
    """Format a salary amount with currency symbol and thousands separators."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}


# --- Chat - Fix Demo ---
def days_until_work_anniversary(emp: Employee) -> int:
    today = date.today()
    next_anniversary = emp.hire_date.replace(year=today.year)
    if next_anniversary < today:
        next_anniversary = next_anniversary.replace(year=today.year + 1)
    return (today - next_anniversary).days


# --- Chat - Doc Demo ---
def group_employees_by_department(employees: List[Employee]) -> Dict[str, List[Employee]]:
    grouped = {}
    for emp in employees:
        if emp.department not in grouped:
            grouped[emp.department] = []
        grouped[emp.department].append(emp)
    return grouped


def sort_employees(employees: List[Employee], key: str = "last_name", reverse: bool = False) -> List[Employee]:
    valid_keys = {"last_name", "first_name", "salary", "hire_date", "department"}
    if key not in valid_keys:
        logger.warning(f"Invalid sort key '{key}', defaulting to 'last_name'")
        key = "last_name"
    return sorted(employees, key=lambda e: getattr(e, key), reverse=reverse)


def format_employee_table(employees: List[Employee]) -> str:
    if not employees:
        return "No employees to display."

    header = f"{'ID':<6}{'Name':<25}{'Department':<15}{'Salary':<12}{'Active':<8}"
    separator = "-" * len(header)
    rows = []
    for emp in employees:
        name = f"{emp.first_name} {emp.last_name}"
        active = "Yes" if emp.is_active else "No"
        rows.append(f"{emp.id:<6}{name:<25}{emp.department:<15}{emp.salary:<12,.2f}{active:<8}")

    return "\n".join([header, separator] + rows)
