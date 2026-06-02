# Reset Demo Kit
# Restores all demo files to their original "broken" state for re-running the demo.

$ErrorActionPreference = "Stop"

Write-Host "Resetting GitHub Copilot Demo Kit..." -ForegroundColor Cyan

# Check we're in the right directory
if (-not (Test-Path "cli.py")) {
    Write-Host "ERROR: Run this script from the github-copilot-demo-kit root directory." -ForegroundColor Red
    exit 1
}

# Reset all tracked files to their committed state
git checkout -- src/
git checkout -- tests/
git checkout -- cli.py
git checkout -- TASKS.md

# Remove any generated files
$filesToRemove = @("employees.json", "*.csv")
foreach ($pattern in $filesToRemove) {
    Get-ChildItem -Path . -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item $_.FullName -Force
        Write-Host "  Removed: $($_.Name)" -ForegroundColor Yellow
    }
}

# Remove any audit log files
if (Test-Path "audit_log.json") {
    Remove-Item "audit_log.json" -Force
    Write-Host "  Removed: audit_log.json" -ForegroundColor Yellow
}

# Clean up __pycache__
Get-ChildItem -Path . -Directory -Filter "__pycache__" -Recurse | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force
}

# Clean up .pytest_cache
if (Test-Path ".pytest_cache") {
    Remove-Item ".pytest_cache" -Recurse -Force
}

# Restore sample data for CLI demos
Copy-Item "sample_employees.json" "employees.json" -Force
Write-Host "  Restored: employees.json (from sample_employees.json)" -ForegroundColor Green

Write-Host ""
Write-Host "Demo reset complete. All files restored to original state." -ForegroundColor Green
Write-Host "Run 'python cli.py --help' to verify." -ForegroundColor Gray
