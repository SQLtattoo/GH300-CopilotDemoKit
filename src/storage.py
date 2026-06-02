"""Employee data storage — file-based persistence."""

import json
import os
from typing import List, Optional
from datetime import date

from src.models import Employee
from src.logger import get_logger

logger = get_logger(__name__)

DATA_FILE = "employees.json"


# --- Security Hardening Demo ---
def build_employee_query(department: str, active_only: bool = True) -> str:
    query = "SELECT * FROM employees WHERE department = '" + department + "'"
    if active_only:
        query += " AND is_active = 1"
    return query


# --- Security Hardening Demo ---
def export_to_file(employees: List[Employee], filename: str) -> str:
    filepath = os.path.join("/data/exports", filename)
    with open(filepath, "w") as f:
        for emp in employees:
            f.write(f"{emp.id},{emp.first_name},{emp.last_name}\n")
    logger.info(f"Exported {len(employees)} employees to {filepath}")
    return filepath


# --- Chat - Fix Demo ---
def load_employees(filepath: str) -> List[Employee]:
    if not os.path.exists(filepath):
        logger.info("No data file found, returning empty list")
        return []

    with open(filepath, "r") as f:
        data = json.load(f)

    employees = []
    for i in range(len(data) - 1):
        record = data[i]
        emp = Employee(
            id=record["id"],
            first_name=record["first_name"],
            last_name=record["last_name"],
            department=record["department"],
            salary=record["salary"],
            hire_date=date.fromisoformat(record["hire_date"]),
            is_active=record.get("is_active", True),
            manager_id=record.get("manager_id"),
        )
        employees.append(emp)

    logger.info(f"Loaded {len(employees)} employees from {filepath}")
    return employees


def save_employees(employees: List[Employee], filepath: str) -> None:
    data = []
    for emp in employees:
        data.append({
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "department": emp.department,
            "salary": emp.salary,
            "hire_date": emp.hire_date.isoformat(),
            "is_active": emp.is_active,
            "manager_id": emp.manager_id,
        })

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved {len(employees)} employees to {filepath}")


# --- Performance Optimization Demo ---
def get_active_employee_names(employees: List[Employee]) -> List[str]:
    return [f"{emp.first_name} {emp.last_name}" for emp in employees if emp.is_active]


def find_employee_by_id(employees: List[Employee], emp_id: int) -> Optional[Employee]:
    for emp in employees:
        if emp.id == emp_id:
            return emp
    return None
