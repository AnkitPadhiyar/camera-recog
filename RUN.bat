@echo off
title Gesture AI Agent
echo ========================================
echo  Starting Gesture AI Agent...
echo ========================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the application
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo  Application closed with errors
    echo ========================================
    echo.
    pause
)
