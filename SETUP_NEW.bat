@echo off
echo ========================================
echo    Gesture AI Agent - Quick Setup
echo ========================================
echo.

echo [1/4] Creating virtual environment...
py -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/4] Upgrading pip...
py -m pip install --upgrade pip

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try: pip install opencv-python mediapipe numpy pyttsx3
    pause
    exit /b 1
)

echo.
echo ========================================
echo     Setup Complete! 
echo ========================================
echo.
echo To run the application:
echo   1. Run: RUN.bat
echo   2. Or manually: venv\Scripts\activate then py main.py
echo.
pause
