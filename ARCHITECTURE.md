# Gesture AI Agent - Architecture Guide

## System Overview

The Gesture AI Agent is a production-grade AI system that recognizes hand gestures, facial expressions, eye blinks, and voice commands to execute system actions in real-time. The architecture follows SOLID principles and maintains clean separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Application                        │
│                     (main.py)                              │
└──────────────┬──────────────────────────────────────────────┘
               │
     ┌─────────┴──────────┬──────────────┬──────────────┐
     │                    │              │              │
     ▼                    ▼              ▼              ▼
┌─────────┐        ┌──────────┐  ┌────────────┐  ┌──────────┐
│ Gesture │        │ Facial   │  │ Voice      │  │ Action   │
│Processor│        │Detector  │  │Commander   │  │Executor  │
└─────────┘        └──────────┘  └────────────┘  └──────────┘
     │                    │              │              │
     │                    │              │              │
     └─────────┬──────────┴──────────────┴──────────────┘
               │
               ▼
        ┌──────────────────┐
        │ Conversation     │
        │ Engine           │
        └──────────────────┘
               │
        ┌──────┴──────┬─────────────────┬──────────────┐
        │             │                 │              │
        ▼             ▼                 ▼              ▼
    ┌────────┐   ┌──────────┐    ┌──────────┐    ┌──────────┐
    │Config  │   │Logger    │    │Music     │    │Mood Log  │
    │Manager │   │Manager   │    │Player    │    │Reader    │
    └────────┘   └──────────┘    └──────────┘    └──────────┘
```

## Module Structure

### Core Modules

#### 1. **main.py** - Application Entry Point
- Initializes all systems
- Manages main event loop
- Handles camera input
- Coordinates between subsystems
- Provides real-time visualization

#### 2. **gesture_processor.py** - Gesture Recognition
```
Responsibilities:
- Hand landmark detection using MediaPipe
- Body pose detection
- Gesture classification (thumbs_up, peace_sign, open_palm, pointing, wave, raise_hand)
- Temporal smoothing for stable detection
- Confidence scoring
- Gesture callback system
```

Key Components:
- `_analyze_hand_gesture()`: Hand gesture classification
- `_analyze_body_gesture()`: Body pose analysis
- `_smooth_gesture()`: Temporal filtering

#### 3. **facial_detector.py** - Facial Analysis
```
Responsibilities:
- Eye blink detection (single, double, triple)
- Facial expression recognition (happy, sad, surprised, angry, neutral)
- Mood classification using pre-trained models
- Confidence scoring for expressions
```

Key Components:
- `detect_blinks()`: Blink pattern detection
- `detect_emotion()`: Expression recognition
- Mood callbacks for action triggering

#### 4. **action_executor.py** - System Action Execution
```
Responsibilities:
- Execute system commands based on gestures
- CRUD operations for notes
- Screenshot capture
- Application launching
- Mood-based actions
- Action logging and history
```

Key Actions:
- Blink actions: open WhatsApp, take screenshot, open notepad
- Gesture actions: mood detection triggers
- Voice actions: cross-platform command execution

#### 5. **voice_commander.py** - Voice Recognition & Control
```
Responsibilities:
- Continuous or single-command voice listening
- Speech-to-text conversion using Google API
- Command parsing and validation
- Voice command callbacks
```

Supported Commands:
- "open whatsapp" → Launch WhatsApp
- "take screenshot" → Capture screen
- "open browser" → Launch web browser
- "open notepad" → Text editor
- "create note" → Note creation

#### 6. **conversation_engine.py** - NLP & Response Generation
```
Responsibilities:
- Local conversation without external APIs
- Context-aware response generation
- Gesture-based conversation routing
- Conversation history management
- Response personalization
```

#### 7. **mood_music_player.py** - Audio Feedback
```
Responsibilities:
- Mood-based music playlist management
- Audio file playback
- Real-time music control
- Integration with gesture/mood detection
```

### Configuration & Utilities

#### 8. **config.py** - Configuration Management
```
Dataclass-based configuration:
- CameraConfig: Input device settings
- GestureConfig: Detection thresholds
- FacialConfig: Expression detection settings
- VoiceConfig: Speech recognition settings
- AudioConfig: Output/music settings
- LoggingConfig: Logger configuration
- ActionConfig: Action execution settings

Features:
- Load from JSON config files
- Save configuration to file
- Override via environment variables
```

#### 9. **logger.py** - Structured Logging
```
Responsibilities:
- Centralized logging setup
- File and console logging
- Rotating file handlers
- Log level management
- Debug information formatting
```

## Data Flow

### Gesture Detection Flow
```
Camera Input
    ↓
OpenCV Frame Reading
    ↓
MediaPipe Processing (Hands + Pose)
    ↓
GestureProcessor Analysis
    ↓
Temporal Smoothing
    ↓
Gesture Callbacks
    ↓
ActionExecutor (Gesture Actions)
```

### Facial Analysis Flow
```
Camera Frame
    ↓
Face Detection (Haar Cascades)
    ↓
Eye Region Extraction
    ↓
Blink Detection
    ↓
Emotion Recognition Model
    ↓
FacialDetector Callbacks
    ↓
Mood-based Actions
```

### Voice Command Flow
```
Audio Input (Microphone)
    ↓
Speech Recognition API
    ↓
Text Conversion
    ↓
Command Parsing
    ↓
VoiceCommander Callback
    ↓
ActionExecutor (Voice Actions)
```

## Design Patterns Used

### 1. **Observer Pattern**
- Gesture callbacks: `register_gesture_callback()`
- Mood callbacks: `register_mood_callback()`
- Allows decoupled event handling

### 2. **Singleton Pattern**
- Configuration: `get_config()`
- Logger: `LoggerManager.get_logger()`
- Ensures single instance per application

### 3. **Strategy Pattern**
- Different action strategies for gestures vs. moods
- Pluggable action executors

### 4. **Builder Pattern**
- Configuration construction with dataclasses
- Flexible configuration loading

## Type System

All modules use Python type hints for:
- Function parameters
- Return types
- Class attributes
- Better IDE support and error detection

## Error Handling

### Hierarchical Error Management
```python
try:
    # Core operation
except SpecificException as e:
    logger.error(f"Error: {e}")
    # Graceful degradation
    # Fallback behavior
except Exception as e:
    logger.exception("Unexpected error")
    # Safe shutdown or default state
```

### Resilience Features
- Camera reconnection on failure
- Graceful module disabling
- Cooldown timers to prevent action floods
- Buffer systems for noisy input

## Performance Considerations

### 1. **Frame Rate Optimization**
- Process every nth frame (`process_every_n_frames`)
- Skip expensive operations on non-critical frames
- Configurable detection thresholds

### 2. **Threading**
- Non-blocking gesture/mood action execution
- Voice recognition in separate thread
- Prevents UI freezing

### 3. **Memory Management**
- Limited gesture history buffer
- Rotating log files
- Capped action log size

### 4. **Input Smoothing**
- Temporal filtering for stable detection
- Confidence-based filtering
- Cooldown periods between actions

## Configuration Management

### Priority Order (Highest to Lowest)
1. Environment variables
2. .env file (python-dotenv)
3. config.json file
4. Hardcoded defaults in config.py

### Loading Configuration
```python
from config import get_config

config = get_config("path/to/config.json")
camera_width = config.camera.width
gesture_threshold = config.gesture.hand_confidence_threshold
```

## Logging Strategy

### Log Levels
- **DEBUG**: Detailed frame processing, detection scores
- **INFO**: Major events, user actions, status changes
- **WARNING**: Recoverable errors, degraded functionality
- **ERROR**: Failed operations, serious issues
- **CRITICAL**: System-level failures

### Log Files
- `gesture_ai.log`: Main application log
- `action_log.json`: Structured action history
- `mood_log.txt`: Mood detection history

## Testing Architecture

### Test Structure
```
tests/
├── unit/
│   ├── test_gesture_processor.py
│   ├── test_facial_detector.py
│   ├── test_action_executor.py
│   ├── test_voice_commander.py
│   └── test_conversation_engine.py
├── integration/
│   ├── test_gesture_to_action.py
│   ├── test_mood_to_action.py
│   └── test_voice_to_action.py
└── fixtures/
    └── mock_data.py
```

### Test Categories
- **Unit Tests**: Individual component functionality
- **Integration Tests**: Cross-module interactions
- **System Tests**: End-to-end workflows

## Deployment

### Local Development
```bash
python -m pip install -r requirements.txt
python main.py
```

### Docker Deployment
```bash
docker-compose up --build
```

### Production Considerations
- Use `--config production.json` for production settings
- Set `LOG_LEVEL=WARNING` in production
- Use separate music library volume
- Monitor log files for errors
- Regular backup of action logs

## Security Considerations

1. **Input Validation**: All user inputs validated before execution
2. **Command Execution**: Whitelist of allowed commands
3. **File Operations**: Path normalization to prevent traversal
4. **Logging**: No sensitive data in logs
5. **API Keys**: Store in .env, never commit

## Future Enhancement Points

1. **Real-time Tracking**: Add multi-person gesture tracking
2. **ML Model Optimization**: Quantized models for faster inference
3. **Speech Synthesis**: Full conversational AI with TTS
4. **Persistent State**: Database for user preferences
5. **Mobile Support**: Mobile gesture recognition
6. **AR Integration**: Augmented reality feedback
7. **Cloud Sync**: Optional cloud-based action history
