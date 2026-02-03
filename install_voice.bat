@echo off
echo ================================================
echo Installing Voice Command Dependencies
echo ================================================
echo.

echo Installing SpeechRecognition...
pip install SpeechRecognition>=3.10.0

echo.
echo Installing PyAudio (this might take a moment)...
echo If PyAudio fails, we'll try alternative method...
pip install PyAudio>=0.2.13

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo PyAudio installation failed. Trying pipwin method...
    pip install pipwin
    pipwin install pyaudio
)

echo.
echo ================================================
echo Testing Installation
echo ================================================
python -c "import speech_recognition; print('✓ SpeechRecognition installed successfully!')"
python -c "import pyaudio; print('✓ PyAudio installed successfully!')"

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo You can now run the application with voice commands:
echo   python main.py
echo.
echo Press 'v' in the application to enable voice commands
echo Press 'l' for single command listening
echo.
pause
