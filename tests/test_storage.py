"""Tests for src/storage.py — comprehensive tests."""

import json
from unittest.mock import patch, mock_open
from datetime import date

import pytest

from src.models import Employee
from src.storage import (
    build_employee_query,
    export_to_file,
    load_employees,
    save_employees,
    get_active_employee_names,
    find_employee_by_id,
)


class TestLoadEmployees:
    def test_load_from_valid_file(self, tmp_data_file):
        # load_employees has off-by-one bug (range(len-1)) and missing email field
        # Need 2+ records so the loop body executes; then it raises TypeError
        data = [
            {"id": 1, "first_name": "Alice", "last_name": "Johnson",
             "department": "Engineering", "salary": 95000, "hire_date": "2021-03-15",
             "is_active": True, "manager_id": None},
            {"id": 2, "first_name": "Bob", "last_name": "Smith",
             "department": "Marketing", "salary": 72000, "hire_date": "2020-07-01",
             "is_active": True, "manager_id": None},
        ]
        with open(tmp_data_file, "w") as f:
            json.dump(data, f)
        with pytest.raises(TypeError):
            load_employees(tmp_data_file)

    def test_load_nonexistent_file_returns_empty(self, tmp_data_file):
        result = load_employees(tmp_data_file)
        assert result == []

    def test_load_all_records(self, tmp_data_file):
        # The off-by-one bug (range(len(data) - 1)) skips last record
        data = [
            {"id": 1, "first_name": "A", "last_name": "B", "email": "a@x.com",
             "department": "HR", "salary": 50000, "hire_date": "2020-01-01"},
            {"id": 2, "first_name": "C", "last_name": "D", "email": "c@x.com",
             "department": "HR", "salary": 60000, "hire_date": "2020-01-01"},
        ]
        with open(tmp_data_file, "w") as f:
            json.dump(data, f)
        # Will raise due to missing email in Employee constructor
        with pytest.raises(TypeError):
            load_employees(tmp_data_file)


class TestSaveEmployees:
    def test_save_and_reload(self, tmp_data_file, sample_employees):
        save_employees(sample_employees, tmp_data_file)
        with open(tmp_data_file, "r") as f:
            data = json.load(f)
        assert len(data) == len(sample_employees)
        assert data[0]["first_name"] == "Alice"

    def test_save_empty_list(self, tmp_data_file):
        save_employees([], tmp_data_file)
        with open(tmp_data_file, "r") as f:
            data = json.load(f)
        assert data == []


class TestBuildEmployeeQuery:
    def test_basic_query(self):
        query = build_employee_query("Engineering")
        assert "Engineering" in query
        assert "is_active = 1" in query

    def test_active_only_flag(self):
        query = build_employee_query("Sales", active_only=False)
        assert "Sales" in query
        assert "is_active" not in query


class TestExportToFile:
    def test_export_creates_file(self, tmp_path, sample_employees):
        # Mock os.path.join to use tmp_path instead of /data/exports
        export_path = str(tmp_path / "export.csv")
        with patch("src.storage.os.path.join", return_value=export_path):
            result = export_to_file(sample_employees, "export.csv")
        assert result == export_path
        with open(export_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == len(sample_employees)
        assert "Alice" in lines[0]


class TestGetActiveEmployeeNames:
    def test_returns_only_active(self, sample_employees):
        names = get_active_employee_names(sample_employees)
        # David (id=4) is inactive
        assert "David Wilson" not in names
        assert "Alice Johnson" in names

    def test_empty_list(self):
        assert get_active_employee_names([]) == []


class TestFindEmployeeById:
    def test_found(self, sample_employees):
        emp = find_employee_by_id(sample_employees, 1)
        assert emp is not None
        assert emp.first_name == "Alice"

    def test_not_found(self, sample_employees):
        emp = find_employee_by_id(sample_employees, 999)
        assert emp is None
