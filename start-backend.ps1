# Start Django API for ESG project (port 8001)
Set-Location $PSScriptRoot\backend

function Test-VenvPython {
    if (-not (Test-Path .\venv\Scripts\python.exe)) { return $false }
    & .\venv\Scripts\python.exe -c "import sys; sys.exit(0)" 2>$null
    return $LASTEXITCODE -eq 0
}

if (-not (Test-VenvPython)) {
    if (Test-Path .\venv) {
        Write-Host "Removing broken venv (was created on another machine)..."
        Remove-Item -Recurse -Force .\venv
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Error @"
Python is not installed or not on PATH.
Install Python 3.10+ from https://www.python.org/downloads/ (check 'Add to PATH'),
then run this script again.
"@
        exit 1
    }
    Write-Host "Creating venv and installing deps..."
    python -m venv venv
    .\venv\Scripts\pip install -r requirements.txt -q
}

if (-not (Test-Path .\db.sqlite3)) {
    Write-Host "Running migrations and seed..."
    .\venv\Scripts\python manage.py migrate
    .\venv\Scripts\python scripts\seed.py
}
Write-Host "Starting Django on http://127.0.0.1:8001 ..."
.\venv\Scripts\python manage.py runserver 8001
