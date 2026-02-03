# Quick Start Guide - Gesture Recognition with Facial Detection

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install opencv-python numpy scipy
```

### 2. Run the Application
```bash
python main.py
```

## 📋 Feature Overview

### Hand Gestures
- **Thumbs Up** 👍 - Positive response
- **Peace Sign** ✌️ - Victory/Peace
- **Open Palm** ✋ - Welcoming
- **Pointing** 👉 - Directional
- **Raise Hand** 🙋 - Attention

### Eye Blink Actions (AUTOMATIC)
When you blink in front of the camera:

1. **Single Blink** 👁️
   - Opens Camera application
   - Wait 3 seconds before next action

2. **Double Blink** 👁️👁️ (within 1.5 seconds)
   - Takes a Screenshot
   - Saved as `gesture_screenshot_TIMESTAMP.png`

3. **Triple Blink** 👁️👁️👁️ (within 1.5 seconds)
   - Opens Notepad/Text Editor
   - Ready for note-taking

### Facial Expressions (AUTOMATIC)
Your mood is continuously detected:

- **😊 Happy** (Smiling) → Logs positive mood
- **😢 Sad** (Frown) → Records sadness
- **😮 Surprised** (Wide eyes) → Captures screenshot
- **😠 Angry** (Furrowed brows) → Clears notifications
- **😐 Neutral** → No action

## 🎮 Controls

| Key | Action |
|-----|--------|
| **q** | Quit application |
| **r** | Reset blink counter |
| **h** | Show action history |

## 💡 Tips for Best Results

### For Blink Detection:
1. Look directly at the camera
2. Make deliberate, clear blinks
3. For double/triple blinks: Blink quickly within 1.5 seconds
4. Wait 3 seconds between actions (cooldown period)

### For Expression Detection:
1. Show clear facial expressions
2. Good lighting is essential
3. Keep face centered in frame
4. Expressions are smoothed over 5 frames for stability

### For Hand Gestures:
1. Hold gestures steady for 0.5-1 second
2. Keep hands in camera view
3. Plain background works best
4. Maintain 1-2 meter distance

## 🔧 Configuration

### Adjust Cooldown Times
Edit `main.py`:
```python
self.blink_cooldown = 3.0      # Seconds between blink actions
self.mood_cooldown = 5.0       # Seconds between mood actions
self.gesture_cooldown = 2.0    # Seconds between gesture responses
```

### Adjust Blink Sensitivity
Edit `facial_detector.py`:
```python
self.blink_frames_threshold = 2  # Frames for blink (lower = more sensitive)
```

### Change Blink Actions
Edit `action_executor.py`:
```python
self.blink_actions = {
    'single_blink': self.your_function,
    'double_blink': self.another_function,
    'triple_blink': self.third_function
}
```

## 📝 CRUD Operations

### Test CRUD Features:
```bash
python demo_crud.py
```

This demonstrates:
- Creating notes
- Reading notes
- Updating notes
- Deleting notes
- Action logging
- History tracking

## 🐛 Troubleshooting

### "No face detected"
- Check lighting (face should be well-lit)
- Move closer to camera (1-2 meters)
- Look directly at camera
- Remove glasses if causing detection issues

### "Blinks not detected"
- Make more deliberate blinks
- Check face is detected first
- Adjust `blink_frames_threshold` in facial_detector.py
- Ensure eyes are clearly visible

### "Actions trigger too often"
- Increase cooldown times
- Increase `min_hold_frames` in gesture_processor.py
- Increase confidence thresholds

### "Camera not opening"
- Close other apps using camera
- Check camera permissions
- Try different camera index: `cv2.VideoCapture(1)`

## 🎯 Example Workflow

1. **Start application**
   ```bash
   python main.py
   ```

2. **Face camera** - You'll see "Face: DETECTED"

3. **Single blink** - Camera app opens

4. **Smile** - Mood logged as "Happy"

5. **Double blink** - Screenshot captured

6. **Press 'h'** - See your action history

7. **Press 'r'** - Reset blink counter if needed

8. **Press 'q'** - Exit application

## 📊 Action History

All actions are logged automatically:
- View in real-time: Press **'h'** key
- Saved to: `action_log.json`
- Mood logs: `mood_log.txt`

## 🔐 Privacy Note

All processing happens **locally** on your machine:
- No data sent to cloud
- No external API calls
- Camera feed never leaves your computer
- All files saved locally in the application directory

## 🆘 Need Help?

Check the main [README.md](README.md) for:
- Detailed technical documentation
- Customization guides
- Advanced configuration
- API reference

---

**Enjoy your gesture-controlled experience! 🎉**
