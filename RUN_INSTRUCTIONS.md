# ⚠️ IMPORTANT: This is a Python Project, NOT Node.js

## Quick Start (Windows)

### Step 1: Install Python Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application
```powershell
# Make sure virtual environment is activated (you should see (venv) in prompt)
python main.py
```

### Alternative: Use Batch Files

We've provided batch files for easy setup:

```powershell
# Setup (first time only)
.\setup.bat

# Run application
.\RUN.bat
```

## ❌ Common Mistakes

### DON'T Use npm Commands
```powershell
# ❌ WRONG - This is NOT a Node.js project
npm install
npm run dev

# ✅ CORRECT - Use Python pip
pip install -r requirements.txt
python main.py
```

## Troubleshooting

### Issue: "python is not recognized"
**Solution**: Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Issue: "pip install fails"
**Solution**: 
```powershell
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### Issue: "Camera not opening"
**Solution**: 
- Close other apps using the camera
- Check Windows privacy settings for camera permissions

## Full Installation Guide

See [INSTALL.md](INSTALL.md) for complete platform-specific instructions.

## What Each File Does

| File | Purpose | How to Run |
|------|---------|------------|
| `main.py` | Main application | `python main.py` |
| `main_enhanced.py` | Professional version | `python main_enhanced.py` |
| `setup.bat` | Windows setup script | `.\setup.bat` |
| `RUN.bat` | Windows run script | `.\RUN.bat` |
| `requirements.txt` | Python dependencies | `pip install -r requirements.txt` |

## Technologies Used

- **Language**: Python 3.9+
- **Computer Vision**: OpenCV, MediaPipe
- **Speech**: SpeechRecognition, pyttsx3
- **ML**: torch, transformers

**NOT using**: Node.js, npm, JavaScript, React, etc.
