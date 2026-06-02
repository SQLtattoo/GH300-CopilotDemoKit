# Tasks for Agent Mode Demo

Use GitHub Copilot's Agent Mode to complete these multi-step tasks autonomously.
Each task requires planning, editing multiple files, and verifying the result.

---

## Task 1: Add Email Field to Employee

Add an `email: str` field to the Employee model and propagate it through the entire codebase.

**Steps required:**
- Add the field to the `Employee` dataclass in `src/models.py`
- Update `employee_to_dict()` and `create_employee_from_dict()` in `src/models.py`
- Update `load_employees()` and `save_employees()` in `src/storage.py`
- Add `validate_email()` function in `src/validators.py` (RFC 5322 basic check)
- Update `validate_employee_data()` to call `validate_email()`
- Add `--email` argument to the `add` command in `cli.py`
- Update test fixtures in `tests/conftest.py`
- Add test stubs for email validation in `tests/test_validators.py`

---

## Task 2: Add CSV Export Command

Add a `csv-export` CLI command that exports employees to a CSV file with proper escaping.

**Steps required:**
- Add `export_to_csv()` function in `src/storage.py`
- Add `cmd_csv_export()` in `cli.py`
- Register the subcommand in `build_parser()`
- Add `--output` and `--department` filter flags
- Write tests in `tests/test_storage.py`
- Update CLI help text

---

## Task 3: Implement Salary Adjustment with Audit Log

Add a `raise` command that applies a percentage salary increase and logs every change.

**Steps required:**
- Add `apply_salary_adjustment()` in `src/services.py`
- Create an audit log entry format (employee_id, old_salary, new_salary, date, reason)
- Add `save_audit_log()` and `load_audit_log()` in `src/storage.py`
- Add `cmd_raise` in `cli.py` with args: employee_id, percentage, reason
- Validate percentage is between 1-50%
- Write tests covering edge cases
- Update the logger to include audit events

---

## Task 4: Add Department Transfer with Validation

Add a `transfer` command that moves an employee between departments with proper checks.

**Steps required:**
- Add `process_transfer()` in `src/services.py`
- Check that target department exists and has budget capacity
- Check that employee is active
- Update employee record and save
- Add `cmd_transfer` in `cli.py`
- Write validation tests
- Log the transfer event
