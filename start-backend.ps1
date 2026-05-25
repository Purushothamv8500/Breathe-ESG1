# Start Django API for ESG project (port 8001)
Set-Location $PSScriptRoot\backend
if (-not (Test-Path .\venv\Scripts\python.exe)) {
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
