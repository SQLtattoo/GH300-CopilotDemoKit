"""Tests for src/services.py — comprehensive tests including edge cases."""

from datetime import date, timedelta

import pytest

from src.models import Employee, Department
from src.services import (
    generate_department_report,
    find_duplicate_employees,
    process_promotion,
    get_employees_by_salary_range,
    calculate_department_stats,
)


class TestGenerateDepartmentReport:
    def test_report_includes_all_departments(self, sample_employees, sample_departments):
        report = generate_department_report(sample_employees, sample_departments)
        for dept in sample_departments:
            assert dept.name in report

    def test_report_avg_salary_calculation(self, sample_employees, sample_departments):
        report = generate_department_report(sample_employees, sample_departments)
        eng = report["Engineering"]
        # Active engineering employees: Alice(95000), Carol(110000), Eve(88000)
        expected_avg = (95000 + 110000 + 88000) / 3
        assert eng["avg_salary"] == pytest.approx(expected_avg)

    def test_report_empty_department(self, sample_departments):
        report = generate_department_report([], sample_departments)
        for dept_name, data in report.items():
            assert data["active"] == 0
            assert data["avg_salary"] == 0

    def test_budget_usage_calculation(self, sample_employees, sample_departments):
        report = generate_department_report(sample_employees, sample_departments)
        eng = report["Engineering"]
        total_salary = 95000 + 110000 + 88000
        expected_usage = (total_salary / 500000) * 100
        assert eng["budget_usage"] == pytest.approx(expected_usage)

    def test_budget_usage_zero_budget(self, sample_employees):
        departments = [Department(name="Engineering", budget=0.0, head_count=3)]
        report = generate_department_report(sample_employees, departments)
        assert report["Engineering"]["budget_usage"] == 0

    def test_tenure_sorted_descending(self, sample_employees, sample_departments):
        report = generate_department_report(sample_employees, sample_departments)
        eng_tenure = report["Engineering"]["tenure"]
        years = [t[1] for t in eng_tenure]
        assert years == sorted(years, reverse=True)


class TestFindDuplicateEmployees:
    def test_no_duplicates(self, sample_employees):
        result = find_duplicate_employees(sample_employees)
        assert result == []

    def test_detects_duplicates(self):
        employees = [
            Employee(id=1, first_name="Alice", last_name="Johnson", email="a1@x.com", department="Engineering", salary=90000, hire_date=date(2020, 1, 1)),
            Employee(id=2, first_name="Alice", last_name="Johnson", email="a2@x.com", department="Engineering", salary=95000, hire_date=date(2021, 1, 1)),
        ]
        result = find_duplicate_employees(employees)
        assert 1 in result
        assert 2 in result

    def test_empty_list(self):
        assert find_duplicate_employees([]) == []

    def test_same_name_different_department_not_duplicate(self):
        employees = [
            Employee(id=1, first_name="Alice", last_name="Johnson", email="a1@x.com", department="Engineering", salary=90000, hire_date=date(2020, 1, 1)),
            Employee(id=2, first_name="Alice", last_name="Johnson", email="a2@x.com", department="Marketing", salary=95000, hire_date=date(2021, 1, 1)),
        ]
        assert find_duplicate_employees(employees) == []


class TestProcessPromotion:
    def test_successful_promotion(self, sample_employee, sample_employees, sample_departments):
        # Alice has tenure > 1 year, is active, moving to Marketing (budget=200000, current total=72000)
        result = process_promotion(sample_employee, "Marketing", sample_employees, sample_departments)
        assert result["success"] is True
        assert result["new_salary"] == pytest.approx(95000 * 1.10)

    def test_inactive_employee_rejected(self, sample_employees, sample_departments):
        inactive = Employee(id=10, first_name="Zack", last_name="Inactive", email="z@x.com",
                            department="Sales", salary=60000, hire_date=date(2019, 1, 1), is_active=False)
        result = process_promotion(inactive, "Engineering", sample_employees, sample_departments)
        assert result["success"] is False
        assert "inactive" in result["message"].lower()

    def test_insufficient_tenure_rejected(self, sample_employees, sample_departments):
        # Hired today — less than 1 year tenure
        new_hire = Employee(id=10, first_name="New", last_name="Hire", email="n@x.com",
                            department="Engineering", salary=70000, hire_date=date.today(), is_active=True)
        result = process_promotion(new_hire, "Marketing", sample_employees, sample_departments)
        assert result["success"] is False
        assert "tenure" in result["message"].lower()

    def test_tenure_exactly_364_days_rejected(self, sample_employees, sample_departments):
        hire_date = date.today() - timedelta(days=364)
        emp = Employee(id=10, first_name="Almost", last_name="Ready", email="a@x.com",
                       department="Engineering", salary=70000, hire_date=hire_date, is_active=True)
        result = process_promotion(emp, "Marketing", sample_employees, sample_departments)
        assert result["success"] is False
        assert "tenure" in result["message"].lower()

    def test_tenure_exactly_365_days_accepted(self, sample_employees, sample_departments):
        hire_date = date.today() - timedelta(days=365)
        emp = Employee(id=10, first_name="Just", last_name="Ready", email="j@x.com",
                       department="Marketing", salary=70000, hire_date=hire_date, is_active=True, manager_id=1)
        result = process_promotion(emp, "Marketing", sample_employees, sample_departments)
        # Should pass tenure check (may fail on other checks depending on budget)
        assert "tenure" not in result["message"].lower()

    def test_tenure_366_days_accepted(self, sample_employees, sample_departments):
        hire_date = date.today() - timedelta(days=366)
        emp = Employee(id=10, first_name="Past", last_name="Ready", email="p@x.com",
                       department="Marketing", salary=70000, hire_date=hire_date, is_active=True, manager_id=1)
        result = process_promotion(emp, "Marketing", sample_employees, sample_departments)
        assert "tenure" not in result["message"].lower()

    def test_invalid_department_rejected(self, sample_employee, sample_employees, sample_departments):
        result = process_promotion(sample_employee, "NonExistent", sample_employees, sample_departments)
        assert result["success"] is False
        assert "does not exist" in result["message"]

    def test_salary_cap_applied(self, sample_employee, sample_employees, sample_departments):
        result = process_promotion(sample_employee, "Marketing", sample_employees, sample_departments,
                                   promotion_percentage=50.0, max_salary_cap=100000.0)
        assert result["success"] is True
        assert result["new_salary"] == 100000.0

    def test_salary_cap_not_applied_when_below(self, sample_employee, sample_employees, sample_departments):
        # 10% of 95000 = 104500; cap at 200000 should not apply
        result = process_promotion(sample_employee, "Marketing", sample_employees, sample_departments,
                                   promotion_percentage=10.0, max_salary_cap=200000.0)
        assert result["success"] is True
        assert result["new_salary"] == pytest.approx(95000 * 1.10)

    def test_salary_cap_exactly_at_cap(self, sample_employees, sample_departments):
        # salary=100000, 10% raise = 110000, cap at 110000 exactly
        emp = Employee(id=10, first_name="Cap", last_name="Test", email="c@x.com",
                       department="Engineering", salary=100000, hire_date=date(2020, 1, 1),
                       is_active=True, manager_id=1)
        result = process_promotion(emp, "Marketing", sample_employees, sample_departments,
                                   promotion_percentage=10.0, max_salary_cap=110000.0)
        assert result["new_salary"] == pytest.approx(110000.0)

    def test_budget_overflow_rejected(self, sample_employees, sample_departments):
        # Marketing budget=200000, Bob already costs 72000. Promoting someone with high salary should exceed.
        expensive = Employee(id=10, first_name="Rich", last_name="Person", email="r@x.com",
                             department="Engineering", salary=200000, hire_date=date(2019, 1, 1),
                             is_active=True, manager_id=1)
        result = process_promotion(expensive, "Marketing", sample_employees, sample_departments)
        # 200000 * 1.10 = 220000; 220000 + 72000 = 292000 > 200000
        assert result["success"] is False
        assert "budget" in result["message"].lower()

    def test_budget_overflow_exactly_at_limit(self, sample_employees):
        # Set budget so projected cost exactly equals budget
        # Bob=72000 in Marketing; promote someone whose new salary = budget - 72000
        target_new_salary = 128000.0  # 128000 + 72000 = 200000
        base_salary = target_new_salary / 1.10  # ~116363.64
        departments = [
            Department(name="Engineering", budget=500000.0, head_count=3),
            Department(name="Marketing", budget=200000.0, head_count=1),
        ]
        emp = Employee(id=10, first_name="Edge", last_name="Case", email="e@x.com",
                       department="Engineering", salary=base_salary, hire_date=date(2019, 1, 1),
                       is_active=True, manager_id=1)
        result = process_promotion(emp, "Marketing", sample_employees, departments)
        # projected = 72000 + 128000 = 200000, budget = 200000 → not exceeded
        assert result["success"] is True

    def test_budget_overflow_one_cent_over(self, sample_employees):
        # Budget exactly 200000; projected should be 200000.01
        departments = [
            Department(name="Engineering", budget=500000.0, head_count=3),
            Department(name="Marketing", budget=200000.0, head_count=1),
        ]
        # Bob=72000; need new_salary such that 72000 + new_salary > 200000
        # new_salary > 128000; base * 1.10 > 128000; base > 116363.636...
        base_salary = 116363.64  # * 1.10 = 128000.004 → 72000 + 128000.004 = 200000.004 > 200000
        emp = Employee(id=10, first_name="Over", last_name="Budget", email="o@x.com",
                       department="Engineering", salary=base_salary, hire_date=date(2019, 1, 1),
                       is_active=True, manager_id=1)
        result = process_promotion(emp, "Marketing", sample_employees, departments)
        assert result["success"] is False
        assert "budget" in result["message"].lower()

    def test_budget_overflow_with_salary_cap_saves_promotion(self, sample_employees):
        # Without cap: exceeds budget. With cap: fits within budget.
        departments = [
            Department(name="Engineering", budget=500000.0, head_count=3),
            Department(name="Marketing", budget=200000.0, head_count=1),
        ]
        # Bob=72000 in Marketing; budget=200000; max available = 128000
        emp = Employee(id=10, first_name="Capped", last_name="Save", email="cs@x.com",
                       department="Engineering", salary=150000, hire_date=date(2019, 1, 1),
                       is_active=True, manager_id=1)
        # Without cap: 150000 * 1.10 = 165000; 72000 + 165000 = 237000 > 200000 → fail
        result_no_cap = process_promotion(emp, "Marketing", sample_employees, departments)
        assert result_no_cap["success"] is False

        # Reset employee department
        emp.department = "Engineering"
        emp.salary = 150000
        # With cap at 120000: 72000 + 120000 = 192000 < 200000 → pass
        result_with_cap = process_promotion(emp, "Marketing", sample_employees, departments,
                                            max_salary_cap=120000.0)
        assert result_with_cap["success"] is True
        assert result_with_cap["new_salary"] == 120000.0

    def test_custom_promotion_percentage(self, sample_employee, sample_employees, sample_departments):
        result = process_promotion(sample_employee, "Marketing", sample_employees, sample_departments,
                                   promotion_percentage=25.0)
        assert result["success"] is True
        assert result["new_salary"] == pytest.approx(95000 * 1.25)

    def test_zero_promotion_percentage(self, sample_employee, sample_employees, sample_departments):
        result = process_promotion(sample_employee, "Marketing", sample_employees, sample_departments,
                                   promotion_percentage=0.0)
        assert result["success"] is True
        assert result["new_salary"] == pytest.approx(95000.0)

    def test_manager_to_empty_department_rejected(self, sample_employee, sample_employees, sample_departments):
        # Alice (manager_id=None) promoted to HR which has no employees → rejected
        result = process_promotion(sample_employee, "HR", sample_employees, sample_departments)
        assert result["success"] is False
        assert "non-manager" in result["message"].lower() or "manager" in result["message"].lower()


class TestGetEmployeesBySalaryRange:
    def test_filters_correctly(self, sample_employees):
        result = get_employees_by_salary_range(sample_employees, 70000, 100000)
        # Active in range: Alice(95000), Bob(72000), Eve(88000)
        assert len(result) == 3

    def test_excludes_inactive(self, sample_employees):
        result = get_employees_by_salary_range(sample_employees, 60000, 70000)
        # David(65000) is inactive, should be excluded
        assert all(e.is_active for e in result)
        assert len(result) == 0

    def test_exact_boundary_values(self, sample_employees):
        result = get_employees_by_salary_range(sample_employees, 95000, 95000)
        assert len(result) == 1
        assert result[0].first_name == "Alice"

    def test_no_matches(self, sample_employees):
        result = get_employees_by_salary_range(sample_employees, 200000, 300000)
        assert result == []


class TestCalculateDepartmentStats:
    def test_basic_stats(self, sample_employees):
        stats = calculate_department_stats(sample_employees, "Engineering")
        assert stats["employee_count"] == 3
        assert stats["total_salary"] == pytest.approx(95000 + 110000 + 88000)
        assert stats["avg_salary"] == pytest.approx((95000 + 110000 + 88000) / 3)

    def test_empty_department(self, sample_employees):
        stats = calculate_department_stats(sample_employees, "HR")
        assert stats["employee_count"] == 0
        assert stats["total_salary"] == 0
        assert stats["avg_salary"] == 0


class TestCalculateDepartmentStats:
    def test_returns_stats_for_department(self, sample_employees):
        pass

    def test_empty_department(self, sample_employees):
        pass
