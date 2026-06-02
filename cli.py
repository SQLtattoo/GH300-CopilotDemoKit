"""CLI entry point for the Employee Management System."""

import argparse
import sys
import json
from datetime import date

from src.models import Employee
from src.services import (
    find_duplicate_employees,
    get_employees_by_salary_range,
    process_promotion,
    generate_department_report,
)
from src.storage import load_employees, save_employees, find_employee_by_id
from src.utils import format_employee_table, sort_employees, group_employees_by_department
from src.validators import validate_employee_data, VALID_DEPARTMENTS
from src.logger import get_logger

logger = get_logger("cli")

DEFAULT_DATA_FILE = "employees.json"


def cmd_list(args):
    """List all employees, optionally filtered."""
    employees = load_employees(args.file)
    if args.department:
        employees = [e for e in employees if e.department == args.department]
    if args.active_only:
        employees = [e for e in employees if e.is_active]
    if args.sort:
        employees = sort_employees(employees, key=args.sort)
    print(format_employee_table(employees))


def cmd_add(args):
    """Add a new employee."""
    data = {
        "first_name": args.first_name,
        "last_name": args.last_name,
        "department": args.department,
        "salary": args.salary,
        "hire_date": args.hire_date or date.today().isoformat(),
    }

    valid, errors = validate_employee_data(data)
    if not valid:
        print("Validation errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    employees = load_employees(args.file)
    new_id = max((e.id for e in employees), default=0) + 1

    emp = Employee(
        id=new_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        department=data["department"],
        salary=float(data["salary"]),
        hire_date=date.fromisoformat(data["hire_date"]),
    )
    employees.append(emp)
    save_employees(employees, args.file)
    print(f"Added employee #{new_id}: {emp.first_name} {emp.last_name}")


# --- Chat - Fix Demo ---
# Bug: typo in method name — calls .isofomat() instead of .isoformat()
def cmd_show(args):
    """Show details of a single employee."""
    employees = load_employees(args.file)
    emp = find_employee_by_id(employees, args.id)
    if not emp:
        print(f"Employee #{args.id} not found.")
        sys.exit(1)

    print(f"ID:         {emp.id}")
    print(f"Name:       {emp.first_name} {emp.last_name}")
    print(f"Department: {emp.department}")
    print(f"Salary:     ${emp.salary:,.2f}")
    print(f"Hire Date:  {emp.hire_date.isofomat()}")  # BUG: typo — isofomat vs isoformat
    print(f"Active:     {'Yes' if emp.is_active else 'No'}")
    print(f"Manager ID: {emp.manager_id or 'None'}")


def cmd_duplicates(args):
    """Find duplicate employees."""
    employees = load_employees(args.file)
    dup_ids = find_duplicate_employees(employees)
    if not dup_ids:
        print("No duplicates found.")
        return
    print(f"Found {len(dup_ids)} duplicate employee(s):")
    for eid in dup_ids:
        emp = find_employee_by_id(employees, eid)
        if emp:
            print(f"  #{emp.id} — {emp.first_name} {emp.last_name} ({emp.department})")


def cmd_report(args):
    """Generate a department report."""
    from src.models import Department

    employees = load_employees(args.file)
    departments = [Department(name=d, budget=1000000.0) for d in VALID_DEPARTMENTS]
    report = generate_department_report(employees, departments)
    print(json.dumps(report, indent=2, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="employee-mgr",
        description="Employee Management System — GitHub Copilot Demo Kit",
    )
    parser.add_argument("--file", default=DEFAULT_DATA_FILE, help="Path to data file")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    list_p = subparsers.add_parser("list", help="List employees")
    list_p.add_argument("--department", choices=VALID_DEPARTMENTS)
    list_p.add_argument("--active-only", action="store_true")
    list_p.add_argument("--sort", choices=["last_name", "salary", "hire_date", "department"])

    # add
    add_p = subparsers.add_parser("add", help="Add a new employee")
    add_p.add_argument("first_name")
    add_p.add_argument("last_name")
    add_p.add_argument("department", choices=VALID_DEPARTMENTS)
    add_p.add_argument("salary", type=float)
    add_p.add_argument("--hire-date", dest="hire_date")

    # show
    show_p = subparsers.add_parser("show", help="Show employee details")
    show_p.add_argument("id", type=int)

    # duplicates
    subparsers.add_parser("duplicates", help="Find duplicate employees")

    # report
    subparsers.add_parser("report", help="Generate department report")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "list": cmd_list,
        "add": cmd_add,
        "show": cmd_show,
        "duplicates": cmd_duplicates,
        "report": cmd_report,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
