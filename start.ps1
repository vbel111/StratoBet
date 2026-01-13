# Backend Quick Start Script

Write-Host "=" -NoNewline; Write-Host "=" * 59
Write-Host "Stratobet Backend - Quick Start"
Write-Host "=" -NoNewline; Write-Host "=" * 59
Write-Host ""

# Check if in backend directory
if (-not (Test-Path "app\main.py")) {
    Write-Host "Error: Please run this script from the backend directory"
    Write-Host "  cd backend"
    Write-Host "  .\start.ps1"
    exit 1
}

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
    Write-Host "  [OK] Virtual environment created"
    Write-Host ""
}

# Activate venv
Write-Host "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"
Write-Host "  [OK] Activated"
Write-Host ""

# Install dependencies
if (-not (Test-Path "venv\Lib\site-packages\fastapi")) {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt -q
    Write-Host "  [OK] Dependencies installed"
    Write-Host ""
}

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..."
    Copy-Item ".env.example" ".env"
    Write-Host "  [OK] .env created"
    Write-Host ""
    Write-Host "IMPORTANT: Update .env with your database password!"
    Write-Host ""
}

# Start server
Write-Host "=" -NoNewline; Write-Host "=" * 59
Write-Host "Starting FastAPI server..."
Write-Host "=" -NoNewline; Write-Host "=" * 59
Write-Host ""
Write-Host "API will be available at:"
Write-Host "  http://localhost:8000"
Write-Host "  http://localhost:8000/docs (Interactive API docs)"
Write-Host ""
Write-Host "Press Ctrl+C to stop"
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
