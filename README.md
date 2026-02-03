# Gesture AI Agent

A self-contained AI agent that detects your gestures, facial expressions, and eye blinks to execute actions and interact with your system in real-time. Now with **Voice Command Support**!

## Features

✨ **Gesture Recognition**
- Hand gestures: Thumbs up, Peace sign, Open palm, Pointing
- Body gestures: Raise hand, Wave
- Real-time detection with temporal smoothing
- Confidence scoring for accurate detection
- Debouncing to prevent false triggers

👁️ **Facial Detection & Analysis**
- **Eye Blink Detection**: Detects single, double, and triple blinks
- **Facial Expression Recognition**: Happy, Sad, Surprised, Angry, Neutral
- **Mood-based Actions**: Automatic responses based on your mood
- Face tracking with OpenCV Haar Cascades

🎤 **Voice Command Control** (NEW!)
- **Natural Language Commands**: Control with your voice
- **Continuous Listening**: Toggle voice recognition on/off
- **Single Command Mode**: Listen for one command at a time
- **Internet-based Recognition**: Uses Google Speech Recognition
- **Supported Commands**:
  - "open whatsapp" - Launch WhatsApp
  - "take screenshot" - Capture screen
  - "open notepad" - Open text editor
  - "open browser" - Launch web browser
  - "create note" - Create new note file

🎬 **Action Execution**
- **Blink Actions**:
  - Single Blink → Opens WhatsApp Desktop
  - Double Blink → Takes Screenshot
  - Triple Blink → Opens Notepad/Text Editor
- **Mood Actions**:
  - Happy → Plays notification
  - Sad → Logs mood to file
  - Surprised → Captures moment (screenshot)
  - Angry → Clears notifications

📝 **CRUD Operations**
- Create, Read, Update, Delete notes via gestures
- Action logging and history tracking
- Export action history to JSON

🤖 **Local Conversation Engine**
- No external APIs or cloud services required
- Context-aware responses based on gestures
- Gesture history tracking
- Conversation logging

🔊 **Text-to-Speech**
- Natural voice responses
- Adjustable speech rate and volume
- Non-blocking speech playback

## Installation

### Prerequisites
- Python 3.8+
- Webcam
- (Optional) Speakers for audio output

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

For audio support on Windows, you may need to install:
```bash
pip install pyaudio
```

## Usage

Start the agent:
```bash
python main.py
```

### Controls
- **Look at camera**: Face detection and expression analysis runs automatically
- **Blink patterns**: Execute different actions based on blink count
- **Make gestures**: Hand gestures for conversation responses
- **Press 'q'**: Quit the application
- **Press 'r'**: Reset blink counter
- **Press 'h'**: Show action history

### Supported Gestures

| Gesture | Description | Response |
|---------|-------------|----------|
| 👍 Thumbs Up | Extended thumb, curled fingers | Positive affirmation |
| ✌️ Peace Sign | Index and middle extended, others curled | Peace/Victory response |
| ✋ Open Palm | All fingers extended | Welcoming response |
| 👉 Pointing | Index extended, others curled | Directional acknowledgment |
| 🙋 Raise Hand | Hand above shoulder | Question/attention response |
| 👋 Wave | Hand waving motion | Greeting response |

### Blink Actions

| Blink Pattern | Action | Description |
|---------------|--------|-------------|
| 👁️ Single Blink | Open Camera | Launches system camera application |
| 👁️👁️ Double Blink | Screenshot | Captures and saves screenshot |
| 👁️👁️👁️ Triple Blink | Open Notepad | Opens text editor |

### Mood Detection

| Mood | Indicator | Action |
|------|-----------|--------|
| 😊 Happy | Smile detected | Plays notification, logs positive mood |
| 😢 Sad | No smile, downturned mouth | Logs mood to file |
| 😮 Surprised | Wide eyes | Captures moment (screenshot) |
| 😠 Angry | Furrowed brows | Clears notifications |
| 😐 Neutral | Default state | No action |

## File Structure

```
vr/
├── main.py                 # Main agent loop and camera handling
├── gesture_processor.py    # Gesture detection and classification
├── conversation_engine.py  # Response generation and TTS
├── facial_detector.py      # Facial detection, blink, and expression analysis
├── action_executor.py      # Action execution and CRUD operations
├── demo_crud.py           # Demo script for CRUD operations
├── requirements.txt        # Python dependencies
├── setup.bat              # Windows setup script
├── setup.sh               # Unix setup script
└── README.md              # This file
```

## How It Works

### Gesture Recognition Pipeline
1. **Frame Capture**: Captures video frames from webcam
2. **Hand Detection**: Color-based detection identifies hand regions
3. **Gesture Classification**: Analyzes hand shape and position
4. **Temporal Smoothing**: Buffers multiple frames to reduce jitter
5. **Debouncing**: Prevents rapid repeated triggers
6. **Response**: Generates contextual conversation responses

### Facial Detection Pipeline
1. **Face Detection**: Haar Cascades detect face region
2. **Feature Extraction**: Identifies eyes, mouth, and facial landmarks
3. **Blink Detection**: Tracks eye closure across frames
4. **Expression Analysis**: Classifies facial expressions
5. **Action Execution**: Triggers system actions based on patterns
6. **Mood Logging**: Records emotional states over time

### Stability Features
- **Gesture Buffer**: Tracks last 5 frames for consistency
- **Minimum Hold Frames**: Requires 3+ consecutive frames for confirmation
- **Confidence Averaging**: Averages scores across frames
- **Cooldown Timers**: Prevents action spam (2-5 second intervals)
- **Frame Skipping**: Processes every 2nd frame for better performance

## Customization

### Add New Gestures

Edit [gesture_processor.py](gesture_processor.py):
```python
def _analyze_hand_gesture(self, hands):
    # Add your gesture detection logic
    pass
```

### Modify Blink Actions

Edit [action_executor.py](action_executor.py):
```python
self.blink_actions = {
    'single_blink': self.your_custom_action,
    'double_blink': self.another_action,
}
```

### Add Custom Mood Actions

Edit [action_executor.py](action_executor.py):
```python
self.mood_actions = {
    'happy': self.custom_happy_action,
}
```

### Adjust Detection Sensitivity

In [facial_detector.py](facial_detector.py), modify parameters:
```python
self.blink_frames_threshold = 2  # Frames to confirm blink
scaleFactor=1.1,  # Face detection sensitivity
minNeighbors=5,   # Detection stability
```

## CRUD Operations

### Using Action Executor

```python
from action_executor import ActionExecutor

executor = ActionExecutor()

# Create a note
executor.create_note("My gesture note")

# Read notes
notes = executor.read_notes()

# Update a note
executor.update_note("filename.txt", "Updated content")

# Delete a note
executor.delete_note("filename.txt")

# View action history
history = executor.get_action_history()
```

### Run CRUD Demo

```bash
python demo_crud.py
```

## Performance Tips

- **Lighting**: Bright, even lighting improves face detection
- **Distance**: Keep 1-2 meters from camera for best results
- **Clear Gestures**: Hold gestures steady for 0.5-1 second
- **Face Camera**: Look directly at camera for expression detection
- **Background**: Plain background improves hand detection
- **Reduce Load**: Close other apps using camera/CPU

## Troubleshooting

**Camera not detected:**
- Check camera is plugged in and not used by another application
- Try different camera indices in [main.py](main.py): `cv2.VideoCapture(0)`

**No voice output:**
- Check speakers are connected
- Ensure volume is not muted
- Test with: `python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"`

**Low gesture recognition:**
- Improve lighting conditions
- Make gestures more pronounced
- Adjust confidence thresholds in gesture detection

## Future Enhancements

- [ ] Multi-user gesture recognition
- [ ] Gesture sequences (combining multiple gestures)
- [ ] Voice input for custom commands
- [ ] Learning from user feedback
- [ ] Gesture recording and playback
- [ ] Integration with local LLMs for advanced NLP
- [ ] Gesture-based UI control

## License

Free to use and modify for personal projects.

## Contributing

Feel free to enhance the gesture recognition and add new features!
