@echo off
echo ========================================
echo  Gesture AI Agent - Setup
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please ensure Python and pip are installed
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation complete!
echo ========================================
echo.
echo To start the agent, run:
echo   python main.py
echo.
echo Press any key to exit...
pause
