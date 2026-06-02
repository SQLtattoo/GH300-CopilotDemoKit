"""Employee data models."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


# TODO: Add an "email" field to Employee.



@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
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
    """Create an Employee instance from a raw dictionary."""
    pass


# --- Chat - Doc Demo ---

def employee_to_dict(emp: Employee) -> dict:
    return {
        "id": emp.id,
        "first_name": emp.first_name,
        "last_name": emp.last_name,
        "department": emp.department,
        "salary": emp.salary,
        "hire_date": emp.hire_date.isoformat(),
        "is_active": emp.is_active,
        "manager_id": emp.manager_id,
    }


def calculate_tenure_years(emp: Employee) -> int:
    today = date.today()
    delta = today - emp.hire_date
    return delta.days // 365
