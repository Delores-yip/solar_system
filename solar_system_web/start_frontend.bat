@echo off
REM Frontend Server Start Script

echo ========================================
echo Solar System Web Application
echo Frontend Server
echo ========================================
echo.

cd frontend

echo Starting frontend server at http://localhost:8000
echo.
echo IMPORTANT: Make sure the backend server is running!
echo Backend should be at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m http.server 8000
