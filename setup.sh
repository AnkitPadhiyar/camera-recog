#!/bin/bash
echo "========================================"
echo " Gesture AI Agent - Setup"
echo "========================================"
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    echo "Please ensure Python and pip are installed"
    exit 1
fi

echo ""
echo "========================================"
echo " Installation complete!"
echo "========================================"
echo ""
echo "To start the agent, run:"
echo "  python main.py"
echo ""
