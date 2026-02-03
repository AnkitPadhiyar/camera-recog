@echo off
echo ========================================
echo  Gesture AI Agent - Easy Installer
echo ========================================
echo.
echo This will automatically set up everything you need!
echo.
pause

echo.
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
python --version
echo ✓ Python found!

echo.
echo [2/5] Creating virtual environment...
if exist .venv (
    echo ✓ Virtual environment already exists
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

echo.
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo [4/5] Installing dependencies (this may take a few minutes)...
echo Installing core packages...
python -m pip install --upgrade pip
pip install opencv-python mediapipe numpy pyttsx3 requests
echo.
echo Installing AI/ML packages...
pip install transformers torch --index-url https://download.pytorch.org/whl/cpu
echo.
echo Installing audio packages...
pip install sounddevice SpeechRecognition
pip install PyAudio || echo ⚠ PyAudio installation failed - voice features may not work

echo.
echo [5/5] Creating launcher...
echo @echo off > RUN.bat
echo call .venv\Scripts\activate.bat >> RUN.bat
echo python main.py >> RUN.bat
echo pause >> RUN.bat

echo.
echo ========================================
echo  Installation Complete! ✓
echo ========================================
echo.
echo To start the application, simply run: RUN.bat
echo.
echo Features:
echo  ✓ Gesture Recognition
echo  ✓ Facial Expression Detection
echo  ✓ Blink Actions
echo  ✓ Voice Commands (if PyAudio works)
echo  ✓ Mood-based Music Player
echo.
echo Press any key to start the application now...
pause >nul

start RUN.bat
