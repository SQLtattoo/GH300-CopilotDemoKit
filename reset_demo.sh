#!/usr/bin/env bash
# Reset Demo Kit
# Restores all demo files to their original "broken" state for re-running the demo.

set -e

echo "Resetting GitHub Copilot Demo Kit..."

# Check we're in the right directory
if [ ! -f "cli.py" ]; then
    echo "ERROR: Run this script from the github-copilot-demo-kit root directory."
    exit 1
fi

# Reset all tracked files to their committed state
git checkout -- src/
git checkout -- tests/
git checkout -- cli.py
git checkout -- TASKS.md

# Remove any generated files
for f in employees.json *.csv audit_log.json; do
    if [ -f "$f" ]; then
        rm -f "$f"
        echo "  Removed: $f"
    fi
done

# Clean up __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Clean up .pytest_cache
rm -rf .pytest_cache

# Restore sample data for CLI demos
cp sample_employees.json employees.json
echo "  Restored: employees.json (from sample_employees.json)"

echo ""
echo "Demo reset complete. All files restored to original state."
echo "Run 'python cli.py --help' to verify."
