"""Tests for src/validators.py — comprehensive tests including edge cases."""

import pytest

from src.validators import (
    validate_employee_name,
    validate_salary,
    validate_department,
    validate_employee_data,
    validate_date_string,
    MIN_SALARY,
    MAX_SALARY,
    VALID_DEPARTMENTS,
)


class TestValidateEmployeeName:
    def test_valid_name(self):
        assert validate_employee_name("Alice") == (True, "")

    def test_valid_name_with_hyphen(self):
        assert validate_employee_name("Mary-Jane") == (True, "")

    def test_valid_name_with_apostrophe(self):
        assert validate_employee_name("O'Brien") == (True, "")

    def test_too_short(self):
        valid, msg = validate_employee_name("A")
        assert valid is False
        assert "at least 2 characters" in msg

    def test_empty_string(self):
        valid, msg = validate_employee_name("")
        assert valid is False
        assert "at least 2 characters" in msg

    def test_too_long(self):
        valid, msg = validate_employee_name("A" * 51)
        assert valid is False
        assert "50 characters" in msg

    def test_exactly_50_characters(self):
        assert validate_employee_name("A" * 50) == (True, "")

    def test_exactly_2_characters(self):
        assert validate_employee_name("Al") == (True, "")

    def test_invalid_characters(self):
        valid, msg = validate_employee_name("123Alice")
        assert valid is False
        assert "invalid characters" in msg


class TestValidateSalary:
    def test_valid_salary(self):
        assert validate_salary(75000.0) == (True, "")

    def test_below_minimum(self):
        valid, msg = validate_salary(29999.99)
        assert valid is False
        assert "at least" in msg

    def test_exactly_minimum(self):
        assert validate_salary(MIN_SALARY) == (True, "")

    def test_above_maximum(self):
        valid, msg = validate_salary(500001.0)
        assert valid is False
        assert "not exceed" in msg

    def test_exactly_maximum(self):
        assert validate_salary(MAX_SALARY) == (True, "")

    def test_non_numeric(self):
        valid, msg = validate_salary("not a number")
        assert valid is False
        assert "must be a number" in msg

    def test_none_value(self):
        valid, msg = validate_salary(None)
        assert valid is False
        assert "must be a number" in msg

    def test_string_numeric_coercion(self):
        assert validate_salary("75000") == (True, "")

    def test_zero_salary(self):
        valid, msg = validate_salary(0)
        assert valid is False
        assert "at least" in msg

    def test_negative_salary(self):
        valid, msg = validate_salary(-50000)
        assert valid is False
        assert "at least" in msg

    def test_one_cent_below_minimum(self):
        valid, msg = validate_salary(MIN_SALARY - 0.01)
        assert valid is False

    def test_one_cent_above_maximum(self):
        valid, msg = validate_salary(MAX_SALARY + 0.01)
        assert valid is False


class TestValidateDepartment:
    def test_valid_department(self):
        for dept in VALID_DEPARTMENTS:
            assert validate_department(dept) == (True, "")

    def test_invalid_department(self):
        valid, msg = validate_department("Accounting")
        assert valid is False
        assert "Invalid department" in msg

    def test_case_sensitive(self):
        valid, msg = validate_department("engineering")
        assert valid is False

    def test_empty_string(self):
        valid, msg = validate_department("")
        assert valid is False


class TestValidateEmployeeData:
    def test_valid_data(self, employee_data_dict):
        valid, errors = validate_employee_data(employee_data_dict)
        assert valid is True
        assert errors == []

    def test_multiple_errors(self):
        data = {
            "first_name": "",
            "last_name": "X",
            "salary": "abc",
            "department": "Invalid",
        }
        valid, errors = validate_employee_data(data)
        assert valid is False
        assert len(errors) == 4

    def test_salary_above_cap_in_data(self):
        data = {
            "first_name": "Valid",
            "last_name": "Name",
            "salary": 600000.0,
            "department": "Engineering",
        }
        valid, errors = validate_employee_data(data)
        assert valid is False
        assert any("salary" in e for e in errors)

    def test_salary_below_minimum_in_data(self):
        data = {
            "first_name": "Valid",
            "last_name": "Name",
            "salary": 10000.0,
            "department": "Engineering",
        }
        valid, errors = validate_employee_data(data)
        assert valid is False
        assert any("salary" in e for e in errors)

    def test_missing_salary_key(self):
        data = {
            "first_name": "Valid",
            "last_name": "Name",
            "department": "Engineering",
        }
        valid, errors = validate_employee_data(data)
        assert valid is False
        assert any("salary" in e for e in errors)


class TestValidateDateString:
    def test_valid_date(self):
        assert validate_date_string("2023-01-15") == (True, "")

    def test_invalid_format(self):
        valid, msg = validate_date_string("01/15/2023")
        assert valid is False
        assert "YYYY-MM-DD" in msg

    def test_empty_string(self):
        valid, msg = validate_date_string("")
        assert valid is False
        assert "required" in msg.lower()

    def test_none_value(self):
        valid, msg = validate_date_string(None)
        assert valid is False

    def test_partial_date(self):
        valid, msg = validate_date_string("2023-01")
        assert valid is False

    def test_extra_characters(self):
        valid, msg = validate_date_string("2023-01-15T00:00")
        assert valid is False
