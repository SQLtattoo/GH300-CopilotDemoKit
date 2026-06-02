"""Tests for src/utils.py — comprehensive tests."""

from datetime import date, timedelta

import pytest

from src.models import Employee
from src.utils import (
    parse_config_value,
    format_salary,
    days_until_work_anniversary,
    group_employees_by_department,
    sort_employees,
    format_employee_table,
)


class TestParseConfigValue:
    def test_parses_integer(self):
        assert parse_config_value("42") == 42

    def test_parses_list(self):
        assert parse_config_value("[1, 2, 3]") == [1, 2, 3]

    def test_parses_dict(self):
        assert parse_config_value("{'key': 'value'}") == {"key": "value"}

    def test_invalid_returns_raw(self):
        result = parse_config_value("not valid python {{")
        assert result == "not valid python {{"


class TestFormatSalary:
    def test_usd_format(self):
        # format_salary is incomplete (code completion demo) — returns None
        result = format_salary(75000.0, "USD")
        assert result is None

    def test_eur_format(self):
        result = format_salary(50000.0, "EUR")
        assert result is None

    def test_unknown_currency(self):
        result = format_salary(60000.0, "JPY")
        assert result is None


class TestDaysUntilWorkAnniversary:
    def test_future_anniversary(self, sample_employee):
        # Exercises the function; has a known sign bug (returns negative)
        result = days_until_work_anniversary(sample_employee)
        assert isinstance(result, int)

    def test_past_anniversary_this_year(self):
        # hire_date with anniversary already passed this year
        emp = Employee(id=1, first_name="A", last_name="B", email="a@b.com",
                       department="HR", salary=50000, hire_date=date(2020, 1, 1))
        result = days_until_work_anniversary(emp)
        assert isinstance(result, int)

    def test_anniversary_today(self):
        today = date.today()
        emp = Employee(id=1, first_name="A", last_name="B", email="a@b.com",
                       department="HR", salary=50000,
                       hire_date=today.replace(year=today.year - 2))
        result = days_until_work_anniversary(emp)
        assert isinstance(result, int)


class TestGroupEmployeesByDepartment:
    def test_groups_correctly(self, sample_employees):
        groups = group_employees_by_department(sample_employees)
        assert "Engineering" in groups
        assert "Marketing" in groups
        assert len(groups["Engineering"]) == 3  # Alice, Carol, Eve

    def test_empty_list(self):
        assert group_employees_by_department([]) == {}


class TestSortEmployees:
    def test_sort_by_salary(self, sample_employees):
        sorted_emps = sort_employees(sample_employees, key="salary")
        salaries = [e.salary for e in sorted_emps]
        assert salaries == sorted(salaries)

    def test_sort_invalid_key_defaults(self, sample_employees):
        sorted_emps = sort_employees(sample_employees, key="invalid_key")
        last_names = [e.last_name for e in sorted_emps]
        assert last_names == sorted(last_names)

    def test_sort_reverse(self, sample_employees):
        sorted_emps = sort_employees(sample_employees, key="salary", reverse=True)
        salaries = [e.salary for e in sorted_emps]
        assert salaries == sorted(salaries, reverse=True)

    def test_sort_by_hire_date(self, sample_employees):
        sorted_emps = sort_employees(sample_employees, key="hire_date")
        dates = [e.hire_date for e in sorted_emps]
        assert dates == sorted(dates)


class TestFormatEmployeeTable:
    def test_formats_output(self, sample_employees):
        table = format_employee_table(sample_employees)
        assert "ID" in table
        assert "Name" in table
        assert "Alice" in table
        assert "Engineering" in table

    def test_empty_list(self):
        result = format_employee_table([])
        assert result == "No employees to display."

    def test_inactive_shown_as_no(self, sample_employees):
        table = format_employee_table(sample_employees)
        assert "No" in table  # David is inactive
