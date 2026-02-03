# 🤖 Gesture AI Agent

A real-time AI-powered gesture recognition system that detects hand gestures, facial expressions, eye blinks, and voice commands to execute automated actions.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/opencv-4.8+-green.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎥 Demo

> **For Recruiters:** See [RECRUITER_GUIDE.md](RECRUITER_GUIDE.md) for quick testing instructions (5 minutes setup)

### Key Features:
- 🤚 Real-time hand gesture recognition
- 😊 Facial expression detection (5 emotions)
- 👁️ Eye blink action triggers
- 🎤 Voice command processing
- 🎵 Mood-based music player
- 👓 Works with glasses

---

## ⚡ Quick Start

### One-Click Installation (Windows)
```bash
# Double-click INSTALL.bat
# Then double-click RUN.bat
```

### Manual Installation
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## 🎯 Features

### 1. **Gesture Recognition**
- Thumbs Up 👍
- Peace Sign ✌️
- Open Palm ✋
- Pointing 👉
- Raise Hand 🙋

### 2. **Facial Expression Detection**
- Happy 😊 → Notification sound
- Sad 😢 → Mood logging
- Surprised 😮 → Screenshot capture
- Angry 😠 → Alert dismissal
- Neutral 😐 → No action

### 3. **Blink Actions**
- **Single Blink** → Opens WhatsApp Desktop
- **Double Blink** → Takes Screenshot (saved as `gesture_screenshot_[timestamp].png`)
- **Triple Blink** → Opens Notepad

### 4. **Voice Commands**
- "open whatsapp"
- "take screenshot"
- "open notepad"
- "open browser"
- "create note"

### 5. **Mood-Based Music Player**
- Automatically plays music based on detected emotions
- Supports custom playlist folders
- Mixed-genre and multi-language support

### 6. **Glasses Detection**
- Automatically detects if user is wearing glasses
- Adapts blink detection algorithm accordingly
- Maintains high accuracy with or without glasses

---

## 🛠️ Technical Architecture

### Core Components

```
main.py                  # Main application & UI
├── gesture_processor.py # Hand gesture detection (MediaPipe)
├── facial_detector.py   # Face & expression detection (OpenCV + Haar Cascades)
├── voice_commander.py   # Speech recognition (Google Speech API)
├── action_executor.py   # Action dispatch & execution
├── conversation_engine.py # Text-to-speech responses
└── mood_music_player.py # Music playback system
```

### Technology Stack

**Computer Vision:**
- OpenCV 4.8+ (Face detection, image processing)
- MediaPipe 0.10+ (Hand landmark detection)
- Haar Cascades (Facial feature detection)

**Machine Learning:**
- PyTorch 2.1+ (Deep learning framework)
- Transformers 4.35+ (NLP models)
- NumPy (Numerical computations)

**Audio Processing:**
- pyttsx3 (Text-to-speech)
- SpeechRecognition (Voice input)
- sounddevice (Audio I/O)

**System Integration:**
- Windows API (Action execution)
- Threading (Concurrent processing)
- Subprocess (External app launching)

---

## 📊 Performance Metrics

- **Frame Rate:** 30 FPS (real-time processing)
- **Gesture Detection Latency:** < 100ms
- **Expression Recognition Accuracy:** ~85%
- **Blink Detection Accuracy:** ~90%
- **Multi-threaded:** Non-blocking operations

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `r` | Reset blink counter |
| `h` | Show action history |
| `v` | Toggle voice commands |
| `l` | Listen for single voice command |
| `m` | Toggle music auto-play |
| `n` | Next track |
| `p` | Pause/Resume music |
| `+/-` | Volume control |
| `f` | Set custom music folder |

---

## 📁 Project Structure

```
gesture-ai-agent/
│
├── main.py                      # Entry point
├── gesture_processor.py         # Gesture detection
├── facial_detector.py           # Facial analysis
├── voice_commander.py           # Voice recognition
├── action_executor.py           # Action handling
├── conversation_engine.py       # TTS engine
├── mood_music_player.py         # Music system
│
├── requirements.txt             # Dependencies
├── INSTALL.bat                  # One-click installer
├── RUN.bat                      # Application launcher
├── RECRUITER_GUIDE.md          # Quick start for recruiters
├── README.md                    # This file
│
└── music_library/              # Optional music folder
    ├── happy/
    ├── sad/
    ├── surprised/
    ├── angry/
    └── neutral/
```

---

## 🔧 Configuration

### Custom Music Folder
Create `music_config.txt` with your music folder path:
```
C:\Users\YourName\Music\MyPlaylist
```

Supported formats: MP3, WAV, FLAC, OGG, M4A, WMA, AAC

---

## 🐛 Troubleshooting

### Camera Issues
- **Camera not opening:** Check permissions in Windows Settings
- **Poor detection:** Ensure good lighting and clean camera lens
- **Slow performance:** Close other camera-using applications

### Voice Commands
- **Not working:** PyAudio installation may have failed (optional feature)
- **Poor recognition:** Speak clearly, reduce background noise
- **Requires internet:** Google Speech Recognition needs connectivity

### Glasses Detection
- **False positives:** Adjust lighting, avoid reflective surfaces
- **Blinks not detected:** Try without glasses or adjust threshold

---

## 📈 Future Enhancements

- [ ] Deep learning-based gesture recognition
- [ ] Custom gesture recording
- [ ] Multi-face detection
- [ ] Sign language recognition
- [ ] Mobile app integration
- [ ] Cloud sync for action history
- [ ] Advanced analytics dashboard

---

## 🤝 Contributing

 suggestions are welcome!

---

## 📄 License

MIT License - feel free to use for learning purposes

---

## 👨‍💻 About

**Developer:** Ankit Padhiyar
**Project Type:**  progressive
**Focus Areas:** Computer Vision, Machine Learning, Real-time Processing  
**Status:** Production-Ready Demo

### Key Learning Outcomes:
✅ Real-time computer vision with OpenCV  
✅ Multi-modal input integration  
✅ Production error handling patterns  
✅ Clean architecture & modular design  
✅ Performance optimization techniques  
✅ User experience design  

---

## 📞 Contact

**LinkedIn:** https://www.linkedin.com/in/ankit-padhiyar-752890284/
**GitHub:** AnkitPadhiyar  
**Email:** padhiyarankit04@gmail.com

---


