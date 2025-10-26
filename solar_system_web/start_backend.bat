@echo off
REM Quick Start Script for Solar System Web Application

echo ========================================
echo Solar System Web Application
echo Quick Start Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
) else (
    echo [2/5] Virtual environment already exists.
)
echo.

REM Activate virtual environment and install dependencies
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [4/5] Installing dependencies...
pip install -r requirements.txt
echo.

echo [5/5] Starting Flask server...
echo.
echo ========================================
echo Server starting at http://localhost:5000
echo ========================================
echo.
echo To view the application:
echo 1. Keep this window open (server running)
echo 2. Open a new terminal
echo 3. Navigate to: solar_system_web/frontend
echo 4. Run: python -m http.server 8000
echo 5. Open browser to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
