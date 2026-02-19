# Gesture AI Agent - Web UI Dashboard

A modern, interactive web-based dashboard for controlling and monitoring the Gesture AI Agent in real-time.

## Features

✨ **Live Camera Feed**
- Real-time video streaming from your camera
- Gesture and emotion detection overlays
- Live status indicators

🎮 **System Control**
- Start/Stop gesture recognition
- Toggle voice command recognition
- Real-time system monitoring

📊 **Real-Time Analytics**
- Live gesture detection display with confidence scores
- Emotion recognition with confidence visualization
- Last action tracking with timestamps
- Gesture statistics and breakdown

📈 **Detailed History**
- Complete gesture detection history with timestamps
- Confidence scores for each detection
- Gesture frequency breakdown
- Top detected gestures

🎯 **Status Dashboard**
- Current gesture and emotion display
- Frame processing counter
- Voice command status
- System health indicator

## Installation

### Prerequisites
- Python 3.8+
- All packages from `requirements.txt`
- Flask and Flask-CORS for the web server

### Setup

1. **Install Web Dependencies**
```bash
pip install -r requirements-web.txt
```

Or install Flask and Flask-CORS directly:
```bash
pip install flask flask-cors
```

2. **Ensure Main Dependencies Are Installed**
```bash
pip install -r requirements.txt
```

## Running the Web UI

### Start the Web Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:5000
```

## Dashboard Overview

### Left Panel - System Control
- **Start Agent**: Begin gesture recognition and emotion detection
- **Stop Agent**: Stop all recognition processes
- **Enable Voice**: Activate voice command listening
- **Status Indicators**: Shows agent state, frame count, and voice status

### Center Panel - Live Camera Feed
- Real-time video stream from your camera
- Gesture and emotion detection overlays
- Live indicator showing stream status
- Flipped for selfie view

### Right Panel - Real-Time Detection
- **Gesture Detection**: Shows currently detected gesture with confidence bar
- **Emotion Recognition**: Displays current emotion with confidence visualization
- **Last Action**: Shows most recent gesture or action detected

### Bottom - Statistics & History

#### Statistics Tab
- **Total Gestures**: Count of all detected gestures during session
- **Average Confidence**: Average confidence score of all detections
- **Most Common Gesture**: Most frequently detected gesture
- **Gesture Breakdown**: Top 5 detected gestures with counts

#### Gesture History Tab
- Scrollable table of all detected gestures
- Timestamps for each detection
- Confidence scores
- Newest detections appear at the top

#### Logs Tab
- System event log
- Initialization messages
- Start/Stop events
- Voice command events
- Error and warning messages

## API Endpoints

The web server provides the following REST API endpoints:

### System Control
- `POST /api/init` - Initialize the gesture AI agent
- `POST /api/start` - Start gesture recognition
- `POST /api/stop` - Stop gesture recognition
- `POST /api/voice/toggle` - Toggle voice command recognition

### Monitoring
- `GET /api/status` - Get current system status
- `GET /api/gesture_history?limit=50` - Get gesture detection history
- `GET /api/gesture_stats` - Get gesture statistics
- `GET /api/health` - Health check endpoint

### Video Streaming
- `GET /api/video_feed` - MJPEG stream of camera feed

## Configuration

The web UI uses the same configuration as the main agent. You can modify:
- Camera settings (resolution, FPS)
- Gesture sensitivity
- Confidence thresholds
- Cooldown periods

See `config.py` for available configuration options.

## Browser Compatibility

- Chrome/Chromium 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## Performance Tips

1. **For Best Performance**:
   - Use a modern browser (Chrome recommended)
   - Ensure camera has good lighting
   - Close unnecessary applications
   - Run on a machine with adequate CPU

2. **Network**:
   - Access dashboard from same machine as server for best performance
   - For remote access, ensure network bandwidth is sufficient for video streaming

3. **Camera**:
   - Position camera 0.5-2 meters away
   - Ensure face is well-lit and visible
   - Keep background simple for better detection

## Troubleshooting

### Camera Not Working
- Verify camera is not in use by another application
- Check camera permissions (Windows may show permission dialog)
- Try restarting the browser

### Video Feed Not Streaming
- Check network connection
- Verify port 5000 is not blocked by firewall
- Try accessing from same machine first

### High CPU Usage
- Reduce camera resolution in configuration
- Close other applications
- Disable voice recognition if not needed

### No Gestures Detected
- Ensure good lighting
- Position hand/body clearly in frame
- Check gesture configuration thresholds
- Verify gesture type is supported

## System Requirements

### Minimum
- 4GB RAM
- Dual-core processor
- Webcam with 720p resolution
- 100 Mbps network connection (for local use)

### Recommended
- 8GB+ RAM
- Quad-core processor or better
- 1080p webcam
- Stable internet connection

## File Structure

```
├── app.py                   # Flask web server
├── requirements-web.txt     # Web dependencies
├── templates/
│   └── index.html          # Main dashboard HTML
└── static/
    ├── style.css           # Dashboard styling
    └── app.js              # Frontend JavaScript
```

## Support

For issues or feature requests, please refer to the main project documentation in:
- `README.md` - Main project overview
- `API_REFERENCE.md` - Full API documentation
- `CONTRIBUTING.md` - Contribution guidelines

## License

Same as main Gesture AI Agent project.
