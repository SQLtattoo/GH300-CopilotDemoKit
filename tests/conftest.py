"""Shared test fixtures for the employee management demo."""

import pytest
from datetime import date

from src.models import Employee, Department


@pytest.fixture
def sample_employee():
    return Employee(
        id=1,
        first_name="Alice",
        last_name="Johnson",
        department="Engineering",
        salary=95000.0,
        hire_date=date(2021, 3, 15),
        is_active=True,
        manager_id=None,
    )


@pytest.fixture
def sample_employees():
    return [
        Employee(id=1, first_name="Alice", last_name="Johnson", department="Engineering", salary=95000.0, hire_date=date(2021, 3, 15), is_active=True),
        Employee(id=2, first_name="Bob", last_name="Smith", department="Marketing", salary=72000.0, hire_date=date(2020, 7, 1), is_active=True),
        Employee(id=3, first_name="Carol", last_name="Davis", department="Engineering", salary=110000.0, hire_date=date(2019, 1, 10), is_active=True),
        Employee(id=4, first_name="David", last_name="Wilson", department="Sales", salary=65000.0, hire_date=date(2022, 11, 20), is_active=False),
        Employee(id=5, first_name="Eve", last_name="Martinez", department="Engineering", salary=88000.0, hire_date=date(2023, 5, 8), is_active=True),
    ]


@pytest.fixture
def sample_departments():
    return [
        Department(name="Engineering", budget=500000.0, head_count=3),
        Department(name="Marketing", budget=200000.0, head_count=1),
        Department(name="Sales", budget=300000.0, head_count=1),
        Department(name="HR", budget=150000.0, head_count=0),
    ]


@pytest.fixture
def employee_data_dict():
    return {
        "first_name": "Frank",
        "last_name": "Garcia",
        "department": "HR",
        "salary": 68000.0,
        "hire_date": "2023-09-01",
    }


@pytest.fixture
def tmp_data_file(tmp_path):
    return str(tmp_path / "test_employees.json")
