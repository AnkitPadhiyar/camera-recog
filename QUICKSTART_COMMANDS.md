# 🚀 QUICK START - Copy & Paste These Commands

## ⚠️ This is a Python Project (NOT Node.js)

You tried to run `npm` commands, but this project uses **Python**, not Node.js/npm.

---

## 📋 Step-by-Step Setup

### Step 1: Create Virtual Environment
```powershell
py -m venv venv
```

### Step 2: Activate Virtual Environment
```powershell
venv\Scripts\activate
```
You should see `(venv)` appear in your prompt

### Step 3: Upgrade pip
```powershell
py -m pip install --upgrade pip
```

### Step 4: Install Dependencies
```powershell
pip install opencv-python mediapipe numpy pyttsx3 sounddevice requests
```

Or install everything:
```powershell
pip install -r requirements.txt
```

### Step 5: Run the Application
```powershell
py main.py
```

---

## 🎯 Even Easier: Use Batch Files

### First Time Setup:
```powershell
.\SETUP_NEW.bat
```

### Run Application:
```powershell
.\RUN_NEW.bat
```

---

## 🔧 Current Status

**Your System:**
- ✅ Python 3.14.2 installed (accessed via `py` command)
- ❌ Virtual environment not yet created
- ❌ Dependencies not yet installed

**What You Need to Do:**
```powershell
# Copy and paste this into PowerShell:
py -m venv venv
venv\Scripts\activate
pip install opencv-python mediapipe numpy pyttsx3 sounddevice
py main.py
```

---

## ❌ What NOT to Do

```powershell
# ❌ WRONG - This is NOT a JavaScript/Node.js project
npm install
npm run dev
npm i

# ✅ CORRECT - Use Python commands
pip install -r requirements.txt
py main.py
```

---

## 📦 What Gets Installed

When you run `pip install -r requirements.txt`, you get:

- **opencv-python** - Camera and computer vision
- **mediapipe** - Hand and pose detection  
- **numpy** - Numerical computing
- **pyttsx3** - Text-to-speech
- **SpeechRecognition** - Voice commands
- **sounddevice** - Audio handling

**Total size: ~500MB** (includes ML models)

---

## 🎮 How to Use After Installation

1. **Run the app**: `py main.py`
2. **Camera will open** showing live feed
3. **Show gestures**:
   - 👍 Thumbs up
   - ✌️ Peace sign  
   - 👋 Wave
   - ☝️ Point
   - ✋ Open palm

4. **Speak commands**:
   - "open whatsapp"
   - "take screenshot"
   - "open browser"

5. **Press Q** to quit

---

## 🐛 Troubleshooting

### "py is not recognized"
Install Python from: https://www.python.org/downloads/
✅ Check "Add Python to PATH" during installation

### "pip install fails"
```powershell
# Update pip first
py -m pip install --upgrade pip

# Install packages one by one
pip install opencv-python
pip install mediapipe
pip install numpy
```

### "No module named cv2"
```powershell
pip install opencv-python
```

### "Camera not opening"
- Close other apps using camera (Zoom, Teams, etc.)
- Check Windows Settings > Privacy > Camera permissions

---

## 📞 Need Help?

See detailed guides:
- [INSTALL.md](INSTALL.md) - Platform-specific installation
- [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md) - Running the app
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

---

## ⚡ Copy-Paste Quick Start

```powershell
# Run all commands in sequence
py -m venv venv
venv\Scripts\activate
pip install opencv-python mediapipe numpy pyttsx3 sounddevice requests
py main.py
```

That's it! 🎉
