@echo off
REM Complete Launch Script - Starts both backend and frontend

echo ========================================
echo Solar System Web Application
echo Complete Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo This script will:
echo 1. Setup and start the backend server
echo 2. Open a new window for the frontend server
echo 3. Open your default browser
echo.
echo Press any key to continue...
pause >nul

REM Start backend in a new window
echo Starting backend server...
start "Solar System Backend" cmd /k "cd backend && (if not exist venv python -m venv venv) && call venv\Scripts\activate.bat && pip install -q -r requirements.txt && python app.py"

REM Wait a moment for backend to initialize
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
echo Starting frontend server...
start "Solar System Frontend" cmd /k "cd frontend && python -m http.server 8000"

REM Wait a moment for frontend to start
timeout /t 3 /nobreak >nul

REM Open browser
echo Opening browser...
start http://localhost:8000

echo.
echo ========================================
echo Application launched successfully!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Two command windows are now open:
echo - Solar System Backend (Flask server)
echo - Solar System Frontend (HTTP server)
echo.
echo Close those windows to stop the servers.
echo.
pause
