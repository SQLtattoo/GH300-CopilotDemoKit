---
name: employee-domain
description: Domain knowledge about the employee management system — data model, business rules, and valid values. Invoked when questions involve employee data, departments, or HR logic.
---

# Employee Domain Knowledge

## Data Model

The system manages `Employee` and `Department` entities.

### Employee Fields
| Field | Type | Constraints |
|-------|------|-------------|
| id | int | Auto-incremented, unique |
| first_name | str | 2-50 chars, alpha + spaces/hyphens |
| last_name | str | 2-50 chars, alpha + spaces/hyphens |
| department | str | Must be in VALID_DEPARTMENTS |
| salary | float | 30,000 – 500,000 |
| hire_date | date | ISO format (YYYY-MM-DD) |
| is_active | bool | Default True |
| manager_id | int? | References another Employee.id |

### Department Fields
| Field | Type | Description |
|-------|------|-------------|
| name | str | Must match VALID_DEPARTMENTS |
| budget | float | Total salary budget for department |
| head_count | int | Current active employees |

## Valid Departments

Engineering, Marketing, Sales, HR, Finance, Operations

## Business Rules

1. **Promotion eligibility:** Employee must be active AND have ≥1 year tenure.
2. **Budget constraint:** A promotion cannot cause total department salaries to exceed department budget.
3. **Salary cap:** Promotions respect an optional max_salary_cap parameter.
4. **Duplicate detection:** Two employees are duplicates if they share (first_name, last_name, department).
5. **Manager rule:** A department needs at least one non-manager before a manager can be added.

## Storage

- Data persists as JSON in a flat file (default: `employees.json`)
- All file I/O routes through `src/storage.py`
- No database — query building functions exist for demo purposes only

## Validation Pipeline

1. Validate individual fields (name, salary, department, date)
2. Aggregate errors into a list
3. Return (bool, errors) tuple
