#!/bin/bash

# Gesture AI Agent - Web UI Launcher
# This script installs dependencies and starts the web server

echo ""
echo "========================================"
echo "  Gesture AI Agent - Web UI"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

# Show Python version
python3 --version

echo ""
echo "[1/3] Installing web dependencies..."
pip install -r requirements-web.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install web dependencies"
    exit 1
fi

echo ""
echo "[2/3] Installing main dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "WARNING: Some main dependencies may not have installed correctly"
fi

echo ""
echo "[3/3] Starting Web Server..."
echo ""
echo "========================================"
echo "  Server is running at: http://localhost:5000"
echo "  Open this URL in your web browser"
echo "  Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Start the Flask server
python3 app.py
