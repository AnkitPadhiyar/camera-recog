# Auto-Screenshot Behavior Explained

## Why Screenshots Are Being Captured Automatically

There are **TWO automatic screenshot triggers** in the code:

### 1. **Detection-Triggered Screenshots** (Line 175-188)
```python
# Auto-screenshot on high-confidence detection
if confidence > 0.75:  # When detection confidence is > 75%
    filename = f"detection_{gesture}_{timestamp}.jpg"
    # Saves any time a strong detection is made (smile, surprise, etc)
```

**Triggers when:**
- ✅ Strong emotion detected (confidence > 0.75)
- ✅ Strong gesture detected  
- ✅ No manual toggle needed

**File naming:** `detection_happy_20260223_213045.jpg`

---

### 2. **Periodic Auto-Screenshot** (Line 223-230)
```python
# Auto-screenshot feature (periodic)
if agent_state.get('auto_screenshot', False) and ...
    filename = f"auto_screenshot_{timestamp}.jpg"
    # Saves every 5 seconds IF the button is toggled
```

**Triggers when:**
- ✅ "Auto Screenshot" button is clicked (enabled)
- ✅ Every 5 seconds automatically

**File naming:** `auto_screenshot_20260223_213045.jpg`

---

## Control Screenshot Behavior

### Option 1: Disable Detection-Triggered Screenshots
If you don't want automatic capture on every emotion detection, modify `app.py` line 175:

**Current:**
```python
if confidence > 0.75:  # Always captures
```

**To disable:**
```python
if False:  # Disable automatic detection screenshots
    # Code won't execute
```

Or remove the block entirely:
```python
# Comment out or delete lines 175-188
# Now only manual/periodic screenshots work
```

---

### Option 2: Disable Periodic Auto-Screenshot
If you don't want screenshots every 5 seconds, the periodic feature only works when you click the "Auto Screenshot" button.

**Current behavior:**
- ❌ Periodic screenshots OFF by default
- ✅ Click "Auto Screenshot" button to enable
- ✅ Then it captures every 5 seconds

---

### Option 3: Control Confidence Threshold
Make detection-triggered screenshots only happen at VERY high confidence:

**Current:**
```python
if confidence > 0.75:  # 75% threshold
```

**Make more selective:**
```python
if confidence > 0.90:  # Only capture at 90%+ confidence
```

---

## Current Behavior Summary

| Trigger | Status | Control |
|---------|--------|---------|
| **Detection (>75% confidence)** | 🔴 **ENABLED** (auto) | Remove code block |
| **Periodic (every 5 sec)** | 🟢 **DISABLED** (manual) | Click "Auto Screenshot" button |

---

## Recommended Settings

### For Development/Testing
👉 **Keep both enabled** - helps you see what's being detected

### For Production Use  
👉 **Options:**
1. Keep detection-triggered only (captures emotional moments)
2. Keep periodic only (regular sampling)
3. Disable both and use manual button only

---

## How to Modify

### To Disable Detection Screenshots

Edit `app.py` around line 175:

```python
# Find this block:
# Auto-screenshot on high-confidence detection
if confidence > 0.75:
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"detection_{gesture}_{timestamp}.jpg"
        filepath = os.path.join('screenshots', filename)
        os.makedirs('screenshots', exist_ok=True)
        cv2.imwrite(filepath, frame)
        logger.info(f"Detection screenshot saved: {filename}")
    except Exception as e:
        logger.debug(f"Could not save detection screenshot: {e}")

# Comment it out or change to:
if False:  # Disabled detection screenshots
    pass
```

---

### To Disable Periodic Screenshots (Already Off by Default)

The periodic feature only activates when you click the "Auto Screenshot" button. Don't click it if you don't want periodic captures.

---

## Check What's Being Saved

Screenshots are saved in: **`screenshots/` folder**

Look for:
- `detection_*.jpg` - Emotion/gesture detections (auto)
- `auto_screenshot_*.jpg` - Periodic captures (when button enabled)

---

## What Do You Want?

Choose one:

1. **Disable auto-screenshots completely** → Comment out detection block
2. **Only periodic screenshots** → Keep detection disabled, use "Auto Screenshot" button  
3. **Only detection screenshots** → Leave detection enabled, don't use "Auto Screenshot" button
4. **Keep both, but adjust trigger** → Change confidence threshold (0.75 → 0.90)
5. **Manual screenshots only** → Disable both, use "Take Screenshot" button

---

**Let me know which option you prefer, and I'll modify the code accordingly!**

