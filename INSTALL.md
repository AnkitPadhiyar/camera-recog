# Installation Guide - Gesture AI Agent

Complete step-by-step installation instructions for all platforms.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Install](#quick-install)
3. [Windows Installation](#windows-installation)
4. [Linux Installation](#linux-installation)
5. [macOS Installation](#macos-installation)
6. [Docker Installation](#docker-installation)
7. [Troubleshooting](#troubleshooting)
8. [Verification](#verification)

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, Ubuntu 20.04+, macOS 10.14+
- **Python**: 3.9 or higher
- **RAM**: 8GB
- **Storage**: 5GB free space
- **Webcam**: USB or built-in camera
- **Microphone**: For voice commands (optional)

### Recommended Requirements
- **OS**: Windows 11, Ubuntu 22.04, macOS 12+
- **Python**: 3.11 or higher
- **RAM**: 16GB
- **GPU**: NVIDIA with CUDA support (for faster processing)
- **Webcam**: USB 3.0 with good low-light performance
- **Audio**: External USB microphone for better voice recognition

## Quick Install

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/gesture-ai-agent.git
cd gesture-ai-agent
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python main.py
```

## Windows Installation

### Step-by-Step

#### 1. Install Python
- Download from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation
- Verify installation:
  ```bash
  python --version
  ```

#### 2. Clone Repository
```bash
# Using Git (if installed)
git clone https://github.com/yourusername/gesture-ai-agent.git

# Or download ZIP and extract
# Then navigate to folder
cd gesture-ai-agent
```

#### 3. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

#### 4. Upgrade pip
```bash
python -m pip install --upgrade pip
```

#### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 6. Install PyAudio (if needed)
```bash
# Try this first:
pip install pipwin
pipwin install pyaudio

# If that fails, download from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then: pip install pyaudio-xxxx.whl
```

#### 7. Configure Environment
```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your settings
# (Optional - defaults work for most users)
```

#### 8. Run Application
```bash
python main.py
```

### Windows-Specific Issues

**Issue**: "python is not recognized"
```bash
# Solution: Use full path or reinstall with PATH option
C:\Python311\python.exe --version

# Or add to PATH manually in System Variables
```

**Issue**: PyAudio installation fails
```bash
# Solution: Use Windows-specific wheel
pip install pipwin
pipwin install pyaudio
```

**Issue**: Camera not found
```bash
# Solution: Check Windows privacy settings
# Settings > Privacy & Security > Camera > App permissions
```

## Linux Installation

### Ubuntu/Debian

#### 1. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    libopencv-dev \
    python3-opencv \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libjack0 \
    alsa-lib \
    pulseaudio
```

#### 2. Clone Repository
```bash
git clone https://github.com/yourusername/gesture-ai-agent.git
cd gesture-ai-agent
```

#### 3. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### 4. Upgrade pip
```bash
python -m pip install --upgrade pip
```

#### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 6. Configure Permissions
```bash
# Allow video device access
sudo usermod -a -G video $USER

# For audio devices
sudo usermod -a -G audio $USER

# Logout and login for changes to take effect
```

#### 7. Run Application
```bash
python main.py
```

### Fedora/RedHat

```bash
sudo dnf install -y \
    python3.11 \
    python3-pip \
    opencv-devel \
    alsa-lib-devel \
    pulseaudio-libs-devel

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## macOS Installation

### Prerequisites
- Xcode Command Line Tools
- Homebrew

#### 1. Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Dependencies
```bash
brew install python@3.11
brew install opencv
brew install portaudio
```

#### 3. Clone Repository
```bash
git clone https://github.com/yourusername/gesture-ai-agent.git
cd gesture-ai-agent
```

#### 4. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### 5. Upgrade pip
```bash
python -m pip install --upgrade pip
```

#### 6. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 7. Grant Camera Permissions
- System Preferences > Security & Privacy > Camera
- Allow Terminal or your IDE

#### 8. Run Application
```bash
python main.py
```

### macOS-Specific Notes
- M1/M2 Macs may need architecture-specific builds
- Use: `arch -arm64 python main.py` for native execution

## Docker Installation

### Prerequisites
- Docker Desktop installed
- 4GB RAM allocated to Docker
- Camera permissions enabled

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/gesture-ai-agent.git
cd gesture-ai-agent

# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Docker Configuration
Edit `docker-compose.yml` to:
- Mount music library volume: `-v ./music_library:/app/music_library`
- Mount logs volume: `-v ./logs:/app/logs`
- Configure environment variables

### Volume Mounts
```yaml
volumes:
  - ./music_library:/app/music_library:ro      # Read-only music
  - ./logs:/app/logs                           # Log output
  - ./notes:/app/notes                         # Note storage
  - ./screenshots:/app/screenshots             # Screenshots
  - /dev/video0:/dev/video0                   # Camera device
```

## Troubleshooting

### Camera Issues

**Problem**: "Error: Unable to open camera"
```bash
# Solution 1: Check device
ls /dev/video*  # Linux
system_profiler SPCameraDataType  # macOS

# Solution 2: Change device ID in config
# Edit config.json: "camera": {"device_id": 0}

# Solution 3: Close other apps using camera
```

**Problem**: "Camera is busy"
```bash
# Windows: Restart camera service
# Linux: killall python3
# macOS: Restart Terminal
```

### Audio Issues

**Problem**: "PyAudio not installed"
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Linux
sudo apt-get install libasound2-dev portaudio19-dev
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio
```

**Problem**: "No audio device found"
```bash
# Check available devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Set device ID in config
"audio": {"device_id": 1}
```

### Recognition Issues

**Problem**: "Speech recognition not working"
```bash
# Check internet connection (Google Speech API)
ping google.com

# Test microphone
python -c "import sounddevice; sounddevice.rec(44100)"
```

**Problem**: "Gesture not detected"
```bash
# Solutions:
# 1. Increase lighting
# 2. Lower confidence threshold in config
# 3. Update camera resolution
# 4. Ensure hand is visible to camera
```

### Memory Issues

**Problem**: "Out of memory"
```bash
# Reduce frame resolution
"camera": {"width": 640, "height": 480}

# Reduce gesture buffer size
"gesture": {"buffer_size": 3}

# Reduce action log size
"action": {"max_log_size": 50}
```

### Performance Issues

**Problem**: "Low FPS / laggy"
```bash
# Solutions:
# 1. Lower frame resolution
# 2. Skip frames: "process_every_n_frames": 3
# 3. Use GPU acceleration if available
# 4. Close other applications
```

### Import Errors

**Problem**: "ModuleNotFoundError"
```bash
# Solution: Ensure virtual environment is activated
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

**Problem**: "MediaPipe not found"
```bash
pip install --upgrade mediapipe
```

## Verification

### Test Installation
```bash
# Run test script
python -c "
import cv2
import numpy as np
import mediapipe as mp
print('✓ OpenCV:', cv2.__version__)
print('✓ NumPy:', np.__version__)
print('✓ MediaPipe: installed')
"
```

### Run Diagnostics
```bash
# Check configuration
python -m config

# List available cameras
python -c "import cv2; cam = cv2.VideoCapture(0); print('Camera:', 'OK' if cam.isOpened() else 'FAILED')"

# Check audio devices
python -c "import sounddevice as sd; print('Audio devices:', len(sd.query_devices()))"
```

### First Run Checklist
- [ ] Python 3.9+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Camera working
- [ ] Microphone working (for voice commands)
- [ ] Good lighting for gesture detection
- [ ] `.env` file configured (optional)

## Next Steps

After successful installation:
1. See [Quick Start](QUICKSTART.md) for first steps
2. Read [API Reference](API_REFERENCE.md) for usage
3. Check [Troubleshooting](TROUBLESHOOTING.md) for help
4. Join [Community Discussions](https://github.com/yourusername/gesture-ai-agent/discussions)

## Support

If you encounter issues:
1. Check [Troubleshooting](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/yourusername/gesture-ai-agent/issues)
3. Create a new issue with details:
   - OS and Python version
   - Error message
   - Steps to reproduce
   - System specifications

## Success Indicators

✅ Installation successful when:
- All packages installed without errors
- `python main.py` starts the application
- Camera feed displays in window
- FPS counter shows > 15 FPS
- No error messages in console
