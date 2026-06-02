"""Employee business logic and services."""

from typing import List, Optional
from datetime import date

from src.models import Employee, Department
from src.logger import get_logger

logger = get_logger(__name__)


# --- Chat - Explain Demo ---
def generate_department_report(employees: List[Employee], departments: List[Department]) -> dict:
    return {d.name: {"active": len([e for e in employees if e.department == d.name and e.is_active]), "avg_salary": (sum(e.salary for e in employees if e.department == d.name and e.is_active) / len([e for e in employees if e.department == d.name and e.is_active])) if len([e for e in employees if e.department == d.name and e.is_active]) > 0 else 0, "tenure": sorted([(e.first_name + " " + e.last_name, (date.today() - e.hire_date).days // 365) for e in employees if e.department == d.name and e.is_active], key=lambda x: x[1], reverse=True), "budget_usage": sum(e.salary for e in employees if e.department == d.name and e.is_active) / d.budget * 100 if d.budget > 0 else 0} for d in departments}


# --- Performance Optimization Demo ---
def find_duplicate_employees(employees: List[Employee]) -> List[int]:
    duplicates = []
    for i in range(len(employees)):
        for j in range(i + 1, len(employees)):
            if (employees[i].first_name == employees[j].first_name and
                    employees[i].last_name == employees[j].last_name and
                    employees[i].department == employees[j].department):
                if employees[i].id not in duplicates:
                    duplicates.append(employees[i].id)
                if employees[j].id not in duplicates:
                    duplicates.append(employees[j].id)
    return duplicates


# --- Refactoring Demo ---
def process_promotion(
    employee: Employee,
    new_department: str,
    employees: List[Employee],
    departments: List[Department],
    promotion_percentage: float = 10.0,
    max_salary_cap: Optional[float] = None,
) -> dict:
    result = {"success": False, "message": "", "old_salary": employee.salary, "new_salary": 0}

    if not employee.is_active:
        result["message"] = "Cannot promote inactive employee"
        logger.warning(f"Promotion failed for employee {employee.id}: inactive")
        return result

    tenure_days = (date.today() - employee.hire_date).days
    if tenure_days < 365:
        result["message"] = "Employee must have at least 1 year tenure"
        logger.warning(f"Promotion failed for employee {employee.id}: insufficient tenure")
        return result

    dept_exists = False
    target_dept = None
    for dept in departments:
        if dept.name == new_department:
            dept_exists = True
            target_dept = dept
            break

    if not dept_exists:
        result["message"] = f"Department '{new_department}' does not exist"
        logger.warning(f"Promotion failed: department {new_department} not found")
        return result

    current_dept_employees = [e for e in employees if e.department == new_department and e.is_active]
    current_salary_total = sum(e.salary for e in current_dept_employees)
    new_salary = employee.salary * (1 + promotion_percentage / 100)

    if max_salary_cap is not None and new_salary > max_salary_cap:
        new_salary = max_salary_cap
        logger.info(f"Salary capped at {max_salary_cap} for employee {employee.id}")

    projected_budget = current_salary_total + new_salary
    if target_dept and projected_budget > target_dept.budget:
        result["message"] = "Promotion would exceed department budget"
        logger.warning(f"Promotion failed for employee {employee.id}: budget exceeded")
        return result

    managers_in_dept = [e for e in employees if e.department == new_department and e.manager_id is None and e.is_active]
    if len(managers_in_dept) == 0 and employee.manager_id is None:
        result["message"] = "Department needs at least one non-manager before adding another manager"
        logger.warning(f"Promotion failed for employee {employee.id}: no reports in target dept")
        return result

    employee.department = new_department
    employee.salary = new_salary
    result["success"] = True
    result["new_salary"] = new_salary
    result["message"] = f"Promoted to {new_department} with salary {new_salary:.2f}"
    logger.info(f"Employee {employee.id} promoted to {new_department}, new salary: {new_salary:.2f}")

    return result


# --- Chat - Doc Demo ---
def get_employees_by_salary_range(employees: List[Employee], min_salary, max_salary):
    return [e for e in employees if min_salary <= e.salary <= max_salary and e.is_active]


# --- Code Completion Demo ---
def calculate_department_stats(employees: List[Employee], department: str) -> dict:
    dept_employees = [e for e in employees if e.department == department and e.is_active]
    total_salary = sum(e.salary for e in dept_employees)
