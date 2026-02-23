# Quick Testing Guide - Improved Gesture AI Agent

## Before You Start
- Ensure good lighting in your environment
- Make sure your webcam is working properly
- Your microphone is optional (will be disabled if not available)

---

## How to Run the Application

### Step 1: Start the Application
```powershell
cd "c:\Users\hp\Desktop\ANKIT\TP\New folder\camera\camera-recog"
& "venv\Scripts\python.exe" app.py
```

The application will start on: `http://127.0.0.1:5000`

### Step 2: Open in Browser
Open your web browser and navigate to: **http://localhost:5000**

---

## Testing Each Feature

### Test 1: Facial Recognition
1. **Click "Start Agent"** button
2. **Look at your camera**
3. Wait for your face to be detected (should see green rectangle around face)
4. **Watch the Emotion Details panel** - confidence should fluctuate as you change expressions
5. Try different expressions:
   - **Smile** → Should detect "happy" emotion
   - **Neutral face** → Should detect "neutral"
   - **Raise eyebrows** → Should detect "surprised"

**Expected Results:**
- ✅ Confidence meter shows fluctuating values (not stuck at 0%)
- ✅ Emotions are detected and displayed
- ✅ Confidence percentage changes in real-time

---

### Test 2: Voice Commands
1. **Look at the "Enable Voice" button**
   - If you have a microphone: Button is enabled (orange)
   - If no microphone: Button is disabled (gray) with message
2. **If microphone available, click "Enable Voice"**
3. The button should change to "Disable Voice" (red)
4. Speak a voice command (system will attempt recognition)

**Expected Results:**
- ✅ Button shows correct state (enabled/disabled)
- ✅ Voice status shows "Enabled" or "Disabled"
- ✅ No errors when toggling voice

---

### Test 3: Auto-Screenshot
1. **Click "Auto Screenshot"** button
2. The button should change appearance (gray → blue)
3. Check the `screenshots/` folder in your project directory
4. **Every 5 seconds**, a new screenshot should be created
5. **Smile or show different expressions** and make high-confidence gestures
6. These should be automatically captured with gesture name

**Expected Results:**
- ✅ Screenshots folder has new images
- ✅ Auto-screenshot button toggles state
- ✅ Gesture-triggered screenshots have gesture name in filename
- ✅ Periodic screenshots have "auto_screenshot" in filename

---

### Test 4: Confidence Meter Fluctuation
1. **Start the agent**
2. **Look away from camera** → Confidence should go to 0%
3. **Look at camera** → Confidence should jump up and show variations
4. **Change expressions** → Both gesture and emotion confidence should change
5. **Observe smooth transitions** (not sudden jumps between 0 and 100%)

**Expected Results:**
- ✅ Gesture confidence: 0-50% range when only face detected
- ✅ Gesture confidence: 50%+ when specific gesture detected
- ✅ Emotion confidence: 30-100% range based on expression
- ✅ Smooth updates every ~500ms (not jumpy)

---

### Test 5: Last Action Display
1. **Start the agent**
2. **Look at camera** → Should see "Waiting for action..." initially
3. **Blink multiple times** → Should show "Blink (single_blink/double_blink/etc)"
4. **Smile strongly** → Should show "Gesture: happy" with timestamp
5. **Check the timestamp** → Should update when action occurs

**Expected Results:**
- ✅ Initial message shows "Waiting for action..."
- ✅ Actions are detected and displayed
- ✅ Timestamps update correctly
- ✅ Blinks are recognized
- ✅ Expressions are recognized as gestures

---

## Gesture History

1. **Navigate to "Gesture History" tab**
2. **Perform various gestures/expressions**
3. **Watch the history table update** with:
   - Timestamp of detection
   - Gesture/emotion name
   - Confidence percentage

---

## Statistics

1. **Navigate to "Statistics" tab**
2. **Perform multiple actions**
3. You should see:
   - Total gestures detected (increasing)
   - Average confidence percentage
   - Most common gesture
   - Gesture breakdown (pie chart style)

---

## Troubleshooting

### Issue: Camera not showing
**Solution:**
- Click "Start Agent" button
- Wait 2-3 seconds for camera to initialize
- Check browser console (F12) for errors
- Ensure no other app is using the camera

### Issue: Confidence meter stuck at 0%
**Solution:**
- Look directly at camera
- Ensure good lighting (at least 500 lux)
- Wait 2-3 seconds for face detection
- Try moving your head slightly

### Issue: Voice button disabled
**Solution:**
- This is normal if microphone is not available
- Other features (facial recognition) still work
- Check System Settings → Sound → Microphone access
- Other features continue working without voice

### Issue: Auto-screenshot not working
**Solution:**
- Ensure agent is running (blue indicator)
- Check that auto-screenshot button is pressed (blue)
- Verify write permissions to project folder
- Check `screenshots/` folder for images

### Issue: Emotions not detected
**Solution:**
- Improve lighting (face should be well-lit)
- Get closer to camera
- Make more pronounced expressions
- Try smiling more clearly for "happy" detection

---

## Performance Tips

1. **Reduce other browser tabs** for better performance
2. **Use a good camera** (minimum 640x480)
3. **Ensure adequate lighting** (bright room)
4. **Keep camera clean** and focused
5. **Close unnecessary applications** to free CPU

---

## File Structure

```
screenshots/              - Auto-saved screenshots
├── auto_screenshot_*.jpg
├── gesture_happy_*.jpg
└── gesture_blink_*.jpg

static/
├── app.js               - Frontend logic
└── style.css

templates/
└── index.html           - Web interface

app.py                    - Main Flask application
facial_detector.py        - Facial recognition
gesture_processor.py      - Gesture analysis
voice_commander.py        - Voice recognition
```

---

## Advanced Options

### Change Auto-Screenshot Interval
Modify in `app.py` line with `screenshot_interval`:
```python
agent_state['screenshot_interval'] = 10  # seconds
```

### Adjust Detection Thresholds
Modify in `gesture_processor.py`:
```python
self.gesture_thresholds = {
    'raise_hand': 0.65,    # Lower = more sensitive
    'open_palm': 0.70,
    ...
}
```

### Adjust Facial Detection Sensitivity
Modify in `facial_detector.py`:
```python
faces = self.face_cascade.detectMultiScale(
    gray, 
    scaleFactor=1.1,       # Lower = more sensitive
    minNeighbors=5         # Lower = more detections
)
```

---

## Documentation Files

- `README.md` - General documentation
- `IMPROVEMENTS_APPLIED.md` - Detailed improvements
- `API_REFERENCE.md` - API endpoint documentation
- `ARCHITECTURE.md` - System architecture

---

## Success Indicators ✅

You'll know the improvements are working when you see:

1. ✅ **Confidence meter changes** when you move/change expressions
2. ✅ **Auto-screenshots** appearing in the `screenshots/` folder
3. ✅ **Last action updates** with gestures and timestamps
4. ✅ **Voice button** properly enabled/disabled based on microphone
5. ✅ **Emotion detection** showing different moods
6. ✅ **History updates** with your actions
7. ✅ **No crashes or errors** during normal use

---

## Questions or Issues?

Check the application logs in the terminal where you started the app for detailed information about what's happening.

Happy testing! 🎉

