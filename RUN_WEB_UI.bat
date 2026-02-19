@echo off
REM Gesture AI Agent - Web UI Launcher
REM This script installs dependencies and starts the web server

echo.
echo ========================================
echo  Gesture AI Agent - Web UI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing web dependencies...
pip install -r requirements-web.txt
if errorlevel 1 (
    echo ERROR: Failed to install web dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Checking main dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some main dependencies may not have installed correctly
)

echo.
echo [3/3] Starting Web Server...
echo.
echo ========================================
echo  Server is running at: http://localhost:5000
echo  Open this URL in your web browser
echo ========================================
echo.

REM Start the Flask server
python app.py

pause
