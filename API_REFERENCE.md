# Gesture AI Agent - API Reference Documentation

## Table of Contents
1. [Core Classes](#core-classes)
2. [Configuration System](#configuration-system)
3. [Gesture Processing](#gesture-processing)
4. [Facial Detection](#facial-detection)
5. [Voice Command](#voice-command)
6. [Action Execution](#action-execution)
7. [Conversation Engine](#conversation-engine)
8. [Logging System](#logging-system)

---

## Core Classes

### GestureAIAgent

Main application class that orchestrates all subsystems.

```python
class GestureAIAgent:
    def __init__(self)
    def run(self) -> None
    def stop(self) -> None
    def process_frame(self, frame) -> dict
```

**Example:**
```python
from main import GestureAIAgent

agent = GestureAIAgent()
agent.run()
```

---

## Configuration System

### Config

Centralized configuration management with type safety.

```python
from config import Config, get_config

# Get global config
config = get_config()

# Access subsystem configs
camera_width = config.camera.width
gesture_threshold = config.gesture.hand_confidence_threshold
log_level = config.logging.level
```

### CameraConfig

```python
@dataclass
class CameraConfig:
    width: int = 1280
    height: int = 720
    fps: int = 30
    device_id: int = 0
    retry_count: int = 3
    retry_delay: float = 1.0
```

### GestureConfig

```python
@dataclass
class GestureConfig:
    enable_hand_gestures: bool = True
    enable_body_gestures: bool = True
    hand_confidence_threshold: float = 0.7
    body_confidence_threshold: float = 0.7
    gesture_buffer_size: int = 5
    min_hold_frames: int = 3
    gesture_cooldown: float = 2.0
```

### FacialConfig

```python
@dataclass
class FacialConfig:
    enable_facial_detection: bool = True
    enable_mood_detection: bool = True
    enable_blink_detection: bool = True
    blink_cooldown: float = 3.0
    mood_cooldown: float = 5.0
    mood_confidence_threshold: float = 0.6
```

### VoiceConfig

```python
@dataclass
class VoiceConfig:
    enable_voice_commands: bool = True
    recognition_language: str = "en-US"
    voice_enabled_by_default: bool = False
    microphone_device_index: Optional[int] = None
    timeout: float = 10.0
    phrase_time_limit: float = 5.0
```

---

## Gesture Processing

### GestureProcessor

Detects and classifies hand and body gestures.

```python
from gesture_processor import GestureProcessor

class GestureProcessor:
    def analyze_gesture(self, gesture_data: dict) -> dict
    def register_gesture_callback(self, callback: Callable) -> None
```

**Gesture Types:**
- `thumbs_up`: Thumb pointing upward
- `peace_sign`: Two fingers forming V shape
- `open_palm`: All fingers extended
- `pointing`: Index finger pointing
- `wave`: Hand moving side to side
- `raise_hand`: Arm raised upward
- `neutral`: No recognized gesture

**Example:**
```python
processor = GestureProcessor()

def on_gesture(gesture_type: str, info: dict):
    print(f"Detected: {gesture_type}")
    print(f"Confidence: {info['confidence']}")

processor.register_gesture_callback(on_gesture)
result = processor.analyze_gesture(gesture_data)
```

**Return Value:**
```python
{
    'gesture_type': 'thumbs_up',
    'confidence': 0.92,
    'details': {...},
    'facial_data': {...}
}
```

---

## Facial Detection

### FacialDetector

Detects facial expressions, emotions, and eye blinks.

```python
from facial_detector import FacialDetector

class FacialDetector:
    def detect_expression(self, frame) -> dict
    def detect_blinks(self, frame) -> dict
    def register_mood_callback(self, callback: Callable) -> None
```

**Supported Emotions:**
- `happy`: Smiling face
- `sad`: Frowning face
- `angry`: Angry expression
- `surprised`: Surprised face
- `neutral`: Neutral expression

**Blink Types:**
- `single_blink`: One eye blink
- `double_blink`: Two consecutive blinks
- `triple_blink`: Three consecutive blinks

**Example:**
```python
detector = FacialDetector()

def on_mood(mood: str, confidence: float):
    print(f"Mood: {mood} (confidence: {confidence})")

detector.register_mood_callback(on_mood)
result = detector.detect_expression(frame)
```

**Return Value:**
```python
{
    'expression': 'happy',
    'confidence': 0.87,
    'blink_type': 'single_blink',
    'blink_status': 'detected'
}
```

---

## Voice Command

### VoiceCommander

Processes voice commands and converts speech to text.

```python
from voice_commander import VoiceCommander

class VoiceCommander:
    def __init__(self, command_callback: Callable)
    def start_listening(self) -> None
    def stop_listening(self) -> None
    def is_listening(self) -> bool
    def toggle_listening(self) -> bool
```

**Supported Commands:**
- `"open whatsapp"` → Launch WhatsApp Desktop
- `"take screenshot"` → Capture screen
- `"open browser"` → Launch web browser
- `"open notepad"` → Open text editor
- `"create note"` → Create new note file

**Example:**
```python
def handle_command(command: str, confidence: float):
    print(f"Command: {command} ({confidence})")

commander = VoiceCommander(command_callback=handle_command)
commander.start_listening()
```

**Command Structure:**
```python
{
    'command': 'open whatsapp',
    'confidence': 0.95,
    'raw_text': 'open whatsapp please',
    'timestamp': '2024-02-18 10:30:45'
}
```

---

## Action Execution

### ActionExecutor

Executes system actions based on gestures, moods, and voice commands.

```python
from action_executor import ActionExecutor

class ActionExecutor:
    def handle_gesture(self, gesture_type: str) -> dict
    def execute_blink_action(self, blink_type: str) -> dict
    def execute_mood_action(self, mood: str, confidence: float) -> dict
    
    # CRUD Operations
    def create_note(self, content: str) -> dict
    def read_notes(self) -> List[dict]
    def update_note(self, note_id: str, content: str) -> dict
    def delete_note(self, note_id: str) -> dict
    
    # System Actions
    def open_whatsapp(self) -> dict
    def take_screenshot(self) -> dict
    def open_notepad(self) -> dict
    def open_browser(self) -> dict
    
    # Logging
    def log_action(self, action_type: str, result: dict) -> None
    def get_action_history(self) -> List[dict]
    def clear_action_history(self) -> None
```

**Example:**
```python
executor = ActionExecutor()

# Handle gesture
result = executor.handle_gesture('thumbs_up')

# Execute mood action
result = executor.execute_mood_action('happy', 0.92)

# Create note
note = executor.create_note("Meeting notes about project")

# Get history
history = executor.get_action_history()
```

**Return Value:**
```python
{
    'status': 'success',
    'action': 'open_whatsapp',
    'timestamp': '2024-02-18 10:30:45',
    'details': {...}
}
```

---

## Conversation Engine

### ConversationEngine

Generates contextual responses based on gestures and detections.

```python
from conversation_engine import ConversationEngine

class ConversationEngine:
    def generate_response(self, gesture_info: dict) -> str
    def get_conversation_history(self) -> List[dict]
    def clear_history(self) -> None
    def set_context(self, key: str, value: Any) -> None
```

**Example:**
```python
engine = ConversationEngine()

gesture_info = {
    'gesture_type': 'peace_sign',
    'confidence': 0.95
}

response = engine.generate_response(gesture_info)
print(response)
# Output: "Peace to you too! Always good to see that gesture."
```

---

## Logging System

### LoggerManager

Centralized logging with file and console output.

```python
from logger import LoggerManager, get_logger

# Setup logging
LoggerManager.setup()

# Get logger for a module
logger = get_logger(__name__)

logger.info("Application started")
logger.warning("No gesture detected")
logger.error("Failed to open camera")
logger.exception("Unexpected error occurred")
```

**Log Levels:**
- `DEBUG`: Detailed information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

**Configuration:**
```python
config.logging.level = "INFO"
config.logging.log_file = "gesture_ai.log"
config.logging.max_bytes = 10 * 1024 * 1024  # 10MB
config.logging.backup_count = 5
config.logging.log_to_console = True
config.logging.log_to_file = True
```

---

## Best Practices

### 1. Error Handling
```python
try:
    result = executor.take_screenshot()
except Exception as e:
    logger.error(f"Screenshot failed: {e}")
```

### 2. Configuration Management
```python
# Load custom config
config = get_config("config.json")

# Modify settings programmatically
config.gesture.hand_confidence_threshold = 0.8
```

### 3. Callback Registration
```python
def handle_gesture(gesture_type, info):
    print(f"Gesture: {gesture_type}")

processor.register_gesture_callback(handle_gesture)
```

### 4. Logging Best Practices
```python
logger = get_logger(__name__)

# Good: Include context
logger.info(f"Detected gesture: {gesture_type} (confidence: {confidence})")

# Bad: Too vague
logger.info("Something happened")
```

---

## Common Workflows

### Complete Gesture Detection Workflow
```python
from main import GestureAIAgent
from logger import LoggerManager

# Initialize logging
LoggerManager.setup()

# Create and run agent
agent = GestureAIAgent()
agent.run()
```

### Custom Gesture Handling
```python
from gesture_processor import GestureProcessor
from action_executor import ActionExecutor

processor = GestureProcessor()
executor = ActionExecutor()

def custom_gesture_handler(gesture_type, info):
    if gesture_type == 'thumbs_up':
        executor.open_whatsapp()
    elif gesture_type == 'peace_sign':
        executor.take_screenshot()

processor.register_gesture_callback(custom_gesture_handler)
```

### Voice Command Processing
```python
from voice_commander import VoiceCommander
from action_executor import ActionExecutor

executor = ActionExecutor()

def command_handler(command, confidence):
    if confidence > 0.8:
        executor.handle_voice_command(command)

commander = VoiceCommander(command_callback=command_handler)
commander.start_listening()
```

---

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `CAMERA_OPEN_FAILED` | Cannot open camera device | Check camera permissions and device ID |
| `MEDIAPIPE_ERROR` | MediaPipe initialization failed | Reinstall mediapipe: `pip install --upgrade mediapipe` |
| `GESTURE_TIMEOUT` | Gesture detection timeout | Increase timeout value in config |
| `VOICE_RECOGNITION_ERROR` | Voice recognition failed | Check microphone and internet connection |
| `ACTION_EXECUTION_FAILED` | Action failed to execute | Check system permissions and command validity |

---

## API Versioning

Current Version: **2.0.0**

Breaking changes are documented in the CHANGELOG.md file.

---

For more information, see [ARCHITECTURE.md](ARCHITECTURE.md) and [README.md](README.md)
