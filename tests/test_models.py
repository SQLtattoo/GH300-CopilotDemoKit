"""Tests for src/models.py — comprehensive tests."""

import pytest
from datetime import date

from src.models import Employee, Department, create_employee_from_dict, employee_to_dict, calculate_tenure_years


class TestEmployee:
    def test_create_employee(self, sample_employee):
        assert sample_employee.id == 1
        assert sample_employee.first_name == "Alice"
        assert sample_employee.department == "Engineering"

    def test_employee_default_values(self):
        emp = Employee(id=1, first_name="A", last_name="B", email="a@b.com",
                       department="HR", salary=50000, hire_date=date(2020, 1, 1))
        assert emp.is_active is True
        assert emp.manager_id is None

    def test_employee_to_dict(self, sample_employee):
        d = employee_to_dict(sample_employee)
        assert d["id"] == 1
        assert d["first_name"] == "Alice"
        assert d["hire_date"] == "2021-03-15"
        assert d["is_active"] is True
        assert d["manager_id"] is None

    def test_create_employee_from_dict(self, employee_data_dict):
        emp = create_employee_from_dict(employee_data_dict)
        assert emp.id == 6
        assert emp.first_name == "Frank"
        assert emp.last_name == "Garcia"
        assert emp.email == "frank@example.com"
        assert emp.department == "HR"
        assert emp.salary == 68000.0
        assert emp.hire_date == date(2023, 9, 1)

    def test_create_employee_from_dict_missing_fields(self):
        with pytest.raises(ValueError, match="Missing required fields"):
            create_employee_from_dict({"id": 1, "first_name": "A"})

    def test_create_employee_from_dict_invalid_salary(self):
        data = {
            "id": 1, "first_name": "A", "last_name": "B", "email": "a@b.com",
            "department": "HR", "salary": "not_a_number", "hire_date": "2020-01-01",
        }
        with pytest.raises(ValueError, match="Failed to create employee"):
            create_employee_from_dict(data)

    def test_create_employee_from_dict_invalid_hire_date_type(self):
        data = {
            "id": 1, "first_name": "A", "last_name": "B", "email": "a@b.com",
            "department": "HR", "salary": 50000, "hire_date": 12345,
        }
        with pytest.raises(ValueError, match="Failed to create employee"):
            create_employee_from_dict(data)

    def test_create_employee_from_dict_with_date_object(self):
        data = {
            "id": 1, "first_name": "A", "last_name": "B", "email": "a@b.com",
            "department": "HR", "salary": 50000, "hire_date": date(2020, 1, 1),
        }
        emp = create_employee_from_dict(data)
        assert emp.hire_date == date(2020, 1, 1)

    def test_create_employee_from_dict_with_manager_id(self):
        data = {
            "id": 1, "first_name": "A", "last_name": "B", "email": "a@b.com",
            "department": "HR", "salary": 50000, "hire_date": "2020-01-01",
            "manager_id": 5,
        }
        emp = create_employee_from_dict(data)
        assert emp.manager_id == 5

    def test_calculate_tenure_years(self, sample_employee):
        # hire_date=2021-03-15, today=2026-06-02 → ~5 years
        years = calculate_tenure_years(sample_employee)
        assert years == 5

    def test_calculate_tenure_years_future_date(self):
        emp = Employee(id=1, first_name="A", last_name="B", email="a@b.com",
                       department="HR", salary=50000, hire_date=date(2030, 1, 1))
        with pytest.raises(ValueError, match="future"):
            calculate_tenure_years(emp)

    def test_calculate_tenure_years_today(self):
        emp = Employee(id=1, first_name="A", last_name="B", email="a@b.com",
                       department="HR", salary=50000, hire_date=date.today())
        assert calculate_tenure_years(emp) == 0


class TestDepartment:
    def test_create_department(self):
        dept = Department(name="Engineering", budget=500000.0, head_count=10)
        assert dept.name == "Engineering"
        assert dept.budget == 500000.0
        assert dept.head_count == 10

    def test_department_default_head_count(self):
        dept = Department(name="HR", budget=100000.0)
        assert dept.head_count == 0
