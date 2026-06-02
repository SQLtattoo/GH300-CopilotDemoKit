# GitHub Copilot Demo Kit

A structured Python project for demonstrating GitHub Copilot capabilities in live sessions.

## Quick Setup

```bash
# Clone and enter the project
cd github-copilot-demo-kit

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Verify Installation

```bash
# Check CLI works
python cli.py --help

# Run tests (they will mostly pass with empty bodies)
pytest
```

## Project Structure

```
github-copilot-demo-kit/
├── cli.py                 # CLI entry point
├── src/
│   ├── models.py          # Employee/Department data models
│   ├── services.py        # Business logic
│   ├── storage.py         # File-based persistence
│   ├── utils.py           # Formatting and utilities
│   ├── validators.py      # Input validation
│   └── logger.py          # Shared logging config
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_storage.py
│   ├── test_utils.py
│   └── test_validators.py
├── .github/
│   └── copilot-instructions.md  # Project conventions for Copilot
├── TASKS.md               # Agent Mode task walkthrough
├── requirements.txt
├── pytest.ini
├── reset_demo.ps1         # Reset script (Windows)
└── reset_demo.sh          # Reset script (macOS/Linux)
```

## Usage

```bash
# List employees
python cli.py list

# Add an employee
python cli.py add "Jane" "Doe" Engineering 95000

# Show employee details
python cli.py show 1

# Find duplicates
python cli.py duplicates

# Department report
python cli.py report
```

## Sample Data

Create an `employees.json` in the project root to seed the demo:

```json
[
  {"id": 1, "first_name": "Alice", "last_name": "Johnson", "department": "Engineering", "salary": 95000, "hire_date": "2021-03-15", "is_active": true, "manager_id": null},
  {"id": 2, "first_name": "Bob", "last_name": "Smith", "department": "Marketing", "salary": 72000, "hire_date": "2020-07-01", "is_active": true, "manager_id": 1},
  {"id": 3, "first_name": "Carol", "last_name": "Davis", "department": "Engineering", "salary": 110000, "hire_date": "2019-01-10", "is_active": true, "manager_id": null},
  {"id": 4, "first_name": "David", "last_name": "Wilson", "department": "Sales", "salary": 65000, "hire_date": "2022-11-20", "is_active": false, "manager_id": 2},
  {"id": 5, "first_name": "Eve", "last_name": "Martinez", "department": "Engineering", "salary": 88000, "hire_date": "2023-05-08", "is_active": true, "manager_id": 3}
]
```

## Resetting After a Demo

```powershell
# Windows
.\reset_demo.ps1

# macOS/Linux
./reset_demo.sh
```

## Requirements

- Python 3.9+
- VS Code with GitHub Copilot extension
- GitHub Copilot license (Individual, Business, or Enterprise)
