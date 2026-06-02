"""Employee data models."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    salary: float
    hire_date: date
    is_active: bool = True
    manager_id: Optional[int] = None


@dataclass
class Department:
    name: str
    budget: float
    head_count: int = 0


# --- Code Completion Demo ---
def create_employee_from_dict(data: dict) -> Employee:
    """Create an Employee instance from a raw dictionary.

    Args:
        data: Dictionary containing employee fields. Must include id, first_name,
              last_name, email, department, salary, and hire_date.

    Returns:
        Employee instance constructed from the dictionary.

    Raises:
        ValueError: If required fields are missing or invalid.
        TypeError: If field types cannot be coerced to the expected types.
    """
    required_fields = {
        "id", "first_name", "last_name", "email", "department", "salary", "hire_date"
    }
    missing = required_fields - set(data.keys())
    if missing:
        error_msg = f"Missing required fields: {missing}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        hire_date = data["hire_date"]
        if isinstance(hire_date, str):
            hire_date = date.fromisoformat(hire_date)
        elif not isinstance(hire_date, date):
            raise TypeError("hire_date must be a date or ISO format string")

        return Employee(
            id=int(data["id"]),
            first_name=str(data["first_name"]),
            last_name=str(data["last_name"]),
            email=str(data["email"]),
            department=str(data["department"]),
            salary=float(data["salary"]),
            hire_date=hire_date,
            is_active=bool(data.get("is_active", True)),
            manager_id=int(data["manager_id"]) if data.get("manager_id") is not None else None,
        )
    except (TypeError, ValueError) as e:
        error_msg = f"Failed to create employee from dict: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e


# --- Chat - Doc Demo ---

def employee_to_dict(emp: Employee) -> dict:
    """Convert an Employee instance to a dictionary.

    Args:
        emp: Employee instance to convert.

    Returns:
        Dictionary representation with all fields; hire_date converted to ISO format.
    """
    return {
        "id": emp.id,
        "first_name": emp.first_name,
        "last_name": emp.last_name,
        "email": emp.email,
        "department": emp.department,
        "salary": emp.salary,
        "hire_date": emp.hire_date.isoformat(),
        "is_active": emp.is_active,
        "manager_id": emp.manager_id,
    }


def calculate_tenure_years(emp: Employee) -> int:
    """Calculate the number of complete years an employee has been with the company.

    Args:
        emp: Employee instance.

    Returns:
        Number of complete years since hire_date (approximate, using 365-day year).

    Raises:
        ValueError: If hire_date is in the future.
    """
    today = date.today()
    if emp.hire_date > today:
        error_msg = f"Hire date cannot be in the future: {emp.hire_date}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    delta = today - emp.hire_date
    return delta.days // 365
