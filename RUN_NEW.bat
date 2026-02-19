@echo off
echo ========================================
echo    Gesture AI Agent - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run SETUP_NEW.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Gesture AI Agent...
echo.
echo Controls:
echo   - Press 'Q' to quit
echo   - Speak "open whatsapp", "take screenshot", etc.
echo   - Show gestures to camera (thumbs up, peace sign, etc.)
echo.

py main.py

pause
