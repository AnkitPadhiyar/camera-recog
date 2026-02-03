# Voice Command Integration Setup Guide

## What Changed

Your Gesture AI Agent now supports **verbal commands** and opens **WhatsApp** instead of the camera!

### Key Changes:

1. **Single Blink** → Opens WhatsApp (instead of camera)
2. **Voice Commands** → Control the system with your voice
3. **New Features** → Press 'v' to enable continuous voice listening, 'l' for single command

## Installation

### Step 1: Install Speech Recognition Dependencies

```bash
pip install SpeechRecognition PyAudio
```

**Note for Windows users:** If PyAudio installation fails, use:
```bash
pip install pipwin
pipwin install pyaudio
```

Or download PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### Step 2: Verify Installation

```bash
python -c "import speech_recognition; print('SpeechRecognition installed successfully!')"
```

## Voice Commands Supported

### Application Control
- **"open whatsapp"** or **"whatsapp"** - Opens WhatsApp
- **"open browser"** or **"browser"** - Opens web browser
- **"open notepad"** or **"notepad"** - Opens text editor

### Screen Capture
- **"take screenshot"** or **"screenshot"** - Captures screen
- **"capture screen"** - Same as screenshot

### Note Management
- **"create note"** - Creates a new note file
- **"read notes"** - Shows all saved notes

## How to Use

### Option 1: Continuous Voice Listening
1. Run the application: `python main.py`
2. Press **'v'** to enable voice commands
3. Speak your commands naturally (e.g., "open whatsapp")
4. Press **'v'** again to disable

### Option 2: Single Command Mode
1. Run the application: `python main.py`
2. Press **'l'** when you want to speak
3. Say your command within 10 seconds
4. The system processes it immediately

### Keyboard Controls
- **'v'** - Toggle continuous voice listening ON/OFF
- **'l'** - Listen for single voice command
- **'q'** - Quit application
- **'r'** - Reset blink counter
- **'h'** - Show action history

## Blink Actions

1. **Single Blink** → Opens WhatsApp
2. **Double Blink** → Takes Screenshot
3. **Triple Blink** → Opens Notepad

## Troubleshooting

### Microphone Not Working
1. Check microphone permissions in Windows Settings
2. Ensure default microphone is selected
3. Test with: Windows > Sound > Input > Test your microphone

### Voice Commands Not Recognized
1. Speak clearly and at normal pace
2. Reduce background noise
3. Adjust microphone volume in Windows settings
4. Check internet connection (uses Google Speech Recognition)

### WhatsApp Not Opening
1. Install WhatsApp Desktop from Microsoft Store
2. Or download from: https://www.whatsapp.com/download
3. Ensure WhatsApp is properly installed and can be launched manually

### PyAudio Installation Fails
```bash
# Alternative method for Windows:
pip install pipwin
pipwin install pyaudio

# Or manually download wheel file:
# Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Download appropriate .whl file for your Python version
# Install: pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl
```

## Testing Voice Commands

Run this test script to verify your setup:

```python
from voice_commander import VoiceCommander

# Create voice commander
vc = VoiceCommander()

# Test microphone
vc.test_microphone()

# Listen for a command
print("Say something...")
command = vc.listen_once()
print(f"You said: {command}")
```

## Internet Requirement

Voice recognition requires an internet connection as it uses Google's Speech Recognition API. If you need offline recognition, consider:
- Using CMU Sphinx (offline, less accurate)
- Using Vosk (offline, better accuracy)
- Implementing local Whisper model

## Performance Tips

1. **Reduce background noise** for better recognition
2. **Speak clearly** - natural pace, not too fast
3. **Use keyword variations** - system recognizes multiple phrases
4. **Internet speed** - faster connection = quicker recognition

## Example Session

```
🤖 Gesture AI Agent Started
Features: Hand Gestures | Facial Expressions | Blink Detection | Voice Commands
Blink Actions: Single=WhatsApp | Double=Screenshot | Triple=Notepad

Voice Commands: 'open whatsapp', 'take screenshot', 'open notepad', 'open browser'

Controls:
  'v' - Toggle continuous voice listening
  'l' - Listen for single voice command
  'q' - Quit
  'r' - Reset blink counter
  'h' - Show action history

🎤 Calibrating microphone for ambient noise...
✅ Microphone ready!

[Press 'v' to enable voice commands]

✅ Voice commands ENABLED - speak your commands!
🎤 Listening for command...
✅ Recognized: 'open whatsapp'
🎙️ Voice Command: 'open whatsapp'
✓ Action: WhatsApp opened
```

## Additional Features

### Add Custom Commands

Edit `action_executor.py` and add to `process_voice_command()`:

```python
command_mappings = {
    'your custom phrase': your_custom_function,
    # ... existing mappings
}
```

### Change WhatsApp Trigger

Edit `action_executor.py`:

```python
self.blink_actions = {
    'single_blink': self.open_whatsapp,  # Change this
    'double_blink': self.take_screenshot,
    'triple_blink': self.open_notepad
}
```

## Credits

- Speech Recognition: Google Speech Recognition API
- Voice Input: SpeechRecognition library
- Audio: PyAudio library

Enjoy your voice-controlled Gesture AI Agent! 🎤🤖
