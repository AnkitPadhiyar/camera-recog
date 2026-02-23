"""
Flask API for Gesture AI Agent
Provides REST endpoints for web UI to control and monitor gesture recognition
"""

from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import cv2
import numpy as np
import threading
import time
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
import base64

from main_enhanced import GestureAIAgent
from logger import get_logger

# Try to import MediaPipe for hand detection
try:
    import mediapipe as mp
    if hasattr(mp, 'solutions'):
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        MEDIAPIPE_AVAILABLE = True
    else:
        # Try new API
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision
        mp_hands = None
        mp_drawing = None
        MEDIAPIPE_AVAILABLE = False
except Exception as e:
    print(f"⚠️ MediaPipe not available for hand detection: {e}")
    mp_hands = None
    mp_drawing = None
    MEDIAPIPE_AVAILABLE = False

logger = get_logger(__name__)

app = Flask(__name__)
CORS(app)

# Global agent instance
agent: Optional[GestureAIAgent] = None
agent_thread: Optional[threading.Thread] = None
agent_lock = threading.Lock()

# Shared state
agent_state = {
    'running': False,
    'current_gesture': None,
    'current_emotion': None,
    'gesture_confidence': 0.0,
    'emotion_confidence': 0.0,
    'last_action': 'Waiting for action...',
    'last_action_time': None,
    'voice_enabled': False,
    'frame_count': 0,
    'gesture_history': [],
    'action_history': [],
    'auto_screenshot': False,
    'screenshot_interval': 5  # seconds
}

current_frame = None
frame_lock = threading.Lock()

# Hand detection
hand_detector = None
hand_detection_lock = threading.Lock()


def init_hand_detector():
    """Initialize MediaPipe hand detector."""
    global hand_detector
    if MEDIAPIPE_AVAILABLE and mp_hands is not None:
        try:
            hand_detector = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            logger.info("Hand detector initialized successfully (MediaPipe)")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe hand detector: {e}")
            logger.info("Falling back to OpenCV hand detection")
            return False
    else:
        logger.info("Using OpenCV-based hand detection (MediaPipe not available)")
        return False


def detect_hands_opencv(frame):
    """Simple hand detection using OpenCV skin color detection."""
    try:
        # Convert to HSV for skin detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create mask for skin color
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Also check second range for darker skin tones
        lower_skin2 = np.array([0, 10, 60], dtype=np.uint8)
        upper_skin2 = np.array([25, 200, 255], dtype=np.uint8)
        mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
        mask = cv2.bitwise_or(mask, mask2)
        
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Get largest contour (likely hand)
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Check if contour is large enough to be a hand
            if area > 1000:
                # Get convex hull
                hull = cv2.convexHull(largest_contour)
                
                # Draw on frame for visualization
                cv2.drawContours(frame, [hull], 0, (0, 255, 0), 2)
                
                # Count fingers (defects)
                defects = cv2.convexityDefects(largest_contour, hull)
                finger_count = 0
                
                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        finger_count += 1
                
                # Return hand info as object with attributes
                class HandInfo:
                    def __init__(self, contour, hull, finger_count, area):
                        self.contour = contour
                        self.hull = hull
                        self.finger_count = finger_count
                        self.area = area
                
                return HandInfo(largest_contour, hull, finger_count, area)
        
        return None
    except Exception as e:
        logger.debug(f"OpenCV hand detection error: {e}")
        return None


def init_agent():
    """Initialize the gesture AI agent."""
    global agent
    try:
        if agent is None:
            agent = GestureAIAgent()
            logger.info("Gesture AI Agent initialized")
            
            # Also initialize hand detector
            init_hand_detector()
        return True
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        return False


def run_agent():
    """Run the agent in a separate thread."""
    global agent, current_frame
    
    if agent is None:
        logger.error("Agent not initialized")
        return
    
    # Verify components exist
    if not hasattr(agent, 'gesture_processor') or not hasattr(agent, 'facial_detector'):
        logger.error("Agent components not properly initialized")
        return
    
    agent.running = True
    agent_state['running'] = True
    last_auto_screenshot = time.time()
    
    try:
        if agent.cap is None:
            agent.cap = agent._open_camera()
        
        if agent.cap is None:
            logger.error("Camera not available")
            agent_state['running'] = False
            return
        
        logger.info("Agent started, beginning frame processing")
        
        while agent.running and agent_state['running']:
            ret, frame = agent.cap.read()
            
            if not ret:
                logger.warning("Failed to read frame from camera")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame - only every nth frame for detection performance
            agent.frame_count += 1
            if agent.frame_count % agent.process_every_n_frames == 0:
                try:
                    # Detect facial features
                    facial_features = agent.facial_detector.detect_face_and_features(frame)
                    blink_info = None
                    expression_info = None
                    face_confidence = 0.0
                    
                    if facial_features:
                        # Face detected - update confidence
                        face_x, face_y, face_w, face_h = facial_features.get('face', (0, 0, 0, 0))
                        face_confidence = min(0.95, (face_w * face_h) / (frame.shape[0] * frame.shape[1]) * 5.0)
                        
                        blink_info = agent.facial_detector.detect_blink(facial_features, frame)
                        expression_info = agent.facial_detector.detect_expression(facial_features, frame)
                    
                    # Combine facial data - ENSURE IT'S PROPERLY STRUCTURED
                    facial_data = {
                        'blink': blink_info,
                        'expression': expression_info  # Pass the full expression_info dict
                    }
                    
                    # Detect hand gestures
                    hand_landmarks = None
                    if hand_detector is not None and MEDIAPIPE_AVAILABLE:
                        try:
                            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = hand_detector.process(rgb_frame)
                            hand_landmarks = results
                            
                            # Draw hand landmarks if detected
                            if results.multi_hand_landmarks and mp_drawing:
                                for hand_landmarks_obj in results.multi_hand_landmarks:
                                    mp_drawing.draw_landmarks(
                                        frame,
                                        hand_landmarks_obj,
                                        mp_hands.HAND_CONNECTIONS
                                    )
                        except Exception as e:
                            logger.debug(f"MediaPipe hand detection error: {e}")
                    else:
                        # Fallback to OpenCV hand detection
                        try:
                            hand_info = detect_hands_opencv(frame)
                            if hand_info:
                                # Create a simple object to pass to gesture processor
                                class SimpleHandLandmarks:
                                    def __init__(self, finger_count):
                                        self.multi_hand_landmarks = [SimpleHandLandmark(finger_count)]
                                
                                class SimpleHandLandmark:
                                    def __init__(self, finger_count):
                                        self.finger_count = finger_count
                                
                                if not hasattr(hand_info, 'finger_count'):
                                    hand_info.finger_count = 0
                                hand_landmarks = SimpleHandLandmarks(hand_info.finger_count)
                        except Exception as e:
                            logger.debug(f"OpenCV hand detection error: {e}")
                    
                    # Process gesture using all data (facial + hand)
                    gesture_data = {
                        'pose': None,
                        'hands': hand_landmarks,  # Pass detected hand data
                        'facial': facial_data,
                        'timestamp': time.time()
                    }
                    
                    gesture_info = agent.gesture_processor.analyze_gesture(gesture_data)
                    
                    # Update gesture/emotion state from detected information
                    if gesture_info:
                        gesture = gesture_info.get('gesture_type', 'neutral')
                        confidence = gesture_info.get('confidence', 0.0)
                        
                        # Check if this is an expression (facial gesture)
                        details = gesture_info.get('details', {})
                        is_expression = details.get('type') == 'facial_expression'
                        
                        # Update gesture state if detected (and different from last)
                        if gesture != 'neutral' and confidence > 0.5:
                            if is_expression:
                                # This is a facial expression
                                agent_state['current_emotion'] = gesture
                                agent_state['emotion_confidence'] = confidence
                                agent_state['last_action'] = f"Emotion: {gesture}"
                            else:
                                # This is a hand/body gesture
                                agent.current_gesture = gesture
                                agent_state['current_gesture'] = gesture
                                agent_state['gesture_confidence'] = confidence
                                agent_state['last_action'] = f"Gesture: {gesture}"
                            
                            agent_state['last_action_time'] = datetime.now().isoformat()
                            logger.info(f"Detection: {gesture} (confidence: {confidence:.2f}, type: {'expression' if is_expression else 'gesture'})")
                            
                            # Add to gesture history (for both expressions and gestures)
                            agent_state['gesture_history'].append({
                                'gesture': gesture,
                                'confidence': confidence,
                                'timestamp': agent_state['last_action_time'],
                                'type': 'expression' if is_expression else 'gesture'
                            })
                            
                            # Keep only last 50 entries
                            if len(agent_state['gesture_history']) > 50:
                                agent_state['gesture_history'].pop(0)
                            
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
                        else:
                            # No strong detection - just update confidence based on face
                            if facial_features:
                                agent_state['gesture_confidence'] = face_confidence * 0.5
                            else:
                                agent_state['gesture_confidence'] = max(0, agent_state['gesture_confidence'] - 0.05)
                            
                            agent.current_gesture = None
                            agent_state['current_gesture'] = None
                    else:
                        # No gesture info
                        if facial_features:
                            agent_state['gesture_confidence'] = face_confidence * 0.5
                        else:
                            agent_state['gesture_confidence'] = max(0, agent_state['gesture_confidence'] - 0.05)
                        agent.current_gesture = None
                        agent_state['current_gesture'] = None
                    
                    # Process blinks
                    if blink_info and blink_info.get('blink_detected'):
                        agent_state['last_action'] = f"Blink ({blink_info.get('blink_type', 'single')})"
                        agent_state['last_action_time'] = datetime.now().isoformat()
                        logger.debug(f"Blink detected: {blink_info.get('blink_type')}")
                
                except AttributeError as e:
                    logger.error(f"Component method missing: {e}")
                except Exception as e:
                    logger.error(f"Frame processing error: {e}")
            
            # Auto-screenshot feature (periodic)
            current_time = time.time()
            if agent_state.get('auto_screenshot', False) and (current_time - last_auto_screenshot) >= agent_state.get('screenshot_interval', 5):
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"auto_screenshot_{timestamp}.jpg"
                    filepath = os.path.join('screenshots', filename)
                    os.makedirs('screenshots', exist_ok=True)
                    cv2.imwrite(filepath, frame)
                    logger.debug(f"Auto-screenshot saved: {filename}")
                    last_auto_screenshot = current_time
                except Exception as e:
                    logger.debug(f"Could not save auto-screenshot: {e}")
            
            # Put text on frame for displaying status
            emotion_text = agent_state['current_emotion'] or 'None'
            gesture_text = agent_state['current_gesture'] or 'None'
            gesture_conf = int(agent_state['gesture_confidence'] * 100)
            emotion_conf = int(agent_state['emotion_confidence'] * 100)
            
            # Display on frame
            cv2.putText(frame, f"Gesture: {gesture_text} ({gesture_conf}%)", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Emotion: {emotion_text} ({emotion_conf}%)", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Store frame for streaming
            with frame_lock:
                current_frame = frame.copy()
            
            agent_state['frame_count'] += 1
    
    except Exception as e:
        logger.error(f"Agent runtime error: {e}", exc_info=True)
    finally:
        agent.running = False
        agent_state['running'] = False
        if agent and agent.cap:
            agent.cap.release()
        logger.info("Agent stopped")


def generate_frames():
    """Generate frames for video streaming."""
    while True:
        with frame_lock:
            if current_frame is not None:
                ret, buffer = cv2.imencode('.jpg', current_frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                # Return placeholder if no frame available
                placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(placeholder, 'Start Agent to View Stream', (130, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                ret, buffer = cv2.imencode('.jpg', placeholder)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.03)  # ~30 FPS


# ==================== API ENDPOINTS ====================

@app.route('/')
def index():
    """Serve the web UI."""
    return render_template('index.html')


@app.route('/api/init', methods=['POST'])
def api_init():
    """Initialize the gesture agent."""
    if init_agent():
        return jsonify({'success': True, 'message': 'Agent initialized'})
    else:
        return jsonify({'success': False, 'error': 'Failed to initialize agent'}), 500


@app.route('/api/start', methods=['POST'])
def api_start():
    """Start the gesture recognition process."""
    global agent_thread
    
    with agent_lock:
        if agent_state['running']:
            return jsonify({'success': False, 'error': 'Agent already running'}), 400
        
        if agent is None:
            if not init_agent():
                return jsonify({'success': False, 'error': 'Failed to initialize agent'}), 500
        
        # Start agent thread
        agent_thread = threading.Thread(target=run_agent, daemon=True)
        agent_thread.start()
        
        return jsonify({'success': True, 'message': 'Agent started'})


@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Stop the gesture recognition process."""
    with agent_lock:
        if agent:
            agent.running = False
            agent_state['running'] = False
        
        return jsonify({'success': True, 'message': 'Agent stopped'})


@app.route('/api/video_feed')
def video_feed():
    """Video streaming endpoint."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/screenshot', methods=['POST'])
def api_screenshot():
    """Take a screenshot and save it."""
    global current_frame
    with frame_lock:
        if current_frame is not None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.jpg"
            filepath = os.path.join('screenshots', filename)
            
            # Create screenshots directory if it doesn't exist
            os.makedirs('screenshots', exist_ok=True)
            
            # Save the frame
            cv2.imwrite(filepath, current_frame)
            
            return jsonify({
                'success': True,
                'message': f'Screenshot saved: {filename}',
                'filename': filename,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No frame available'
            }), 400


@app.route('/api/status', methods=['GET'])
def api_status():
    """Get current agent status."""
    return jsonify({
        'running': agent_state['running'],
        'current_gesture': agent_state['current_gesture'],
        'current_emotion': agent_state['current_emotion'],
        'gesture_confidence': agent_state['gesture_confidence'],
        'emotion_confidence': agent_state['emotion_confidence'],
        'last_action': agent_state['last_action'],
        'last_action_time': agent_state['last_action_time'],
        'voice_enabled': agent_state['voice_enabled'],
        'frame_count': agent_state['frame_count']
    })


@app.route('/api/gesture_history', methods=['GET'])
def api_gesture_history():
    """Get gesture detection history."""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({
        'history': agent_state['gesture_history'][-limit:]
    })


@app.route('/api/action_history', methods=['GET'])
def api_action_history():
    """Get action execution history."""
    limit = request.args.get('limit', 100, type=int)
    return jsonify({
        'history': agent_state['action_history'][-limit:]
    })


@app.route('/api/voice/status', methods=['GET'])
def api_voice_status():
    """Get voice command status."""
    if agent is None:
        return jsonify({
            'enabled': False,
            'available': False,
            'listening': False
        })
    
    return jsonify({
        'enabled': agent_state['voice_enabled'],
        'available': agent.voice_commander.is_available(),
        'listening': agent.voice_commander.is_listening if hasattr(agent.voice_commander, 'is_listening') else False
    })


@app.route('/api/screenshot/auto', methods=['POST'])
def api_auto_screenshot_toggle():
    """Toggle automatic screenshot feature."""
    agent_state['auto_screenshot'] = not agent_state.get('auto_screenshot', False)
    
    # Optional: set screenshot interval from request
    interval = request.get_json().get('interval', 5) if request.is_json else 5
    agent_state['screenshot_interval'] = max(1, min(interval, 60))  # Clamp to 1-60 seconds
    
    return jsonify({
        'enabled': agent_state['auto_screenshot'],
        'interval': agent_state['screenshot_interval'],
        'message': f"Auto-screenshot {'enabled' if agent_state['auto_screenshot'] else 'disabled'}"
    })
def api_voice_toggle():
    """Toggle voice command recognition."""
    if agent is None:
        return jsonify({'success': False, 'error': 'Agent not initialized'}), 400
    
    # Check if microphone is available
    if not agent.voice_commander.is_available():
        return jsonify({
            'success': False, 
            'error': 'Microphone not available',
            'enabled': False
        }), 400
    
    try:
        agent_state['voice_enabled'] = not agent_state['voice_enabled']
        
        if agent_state['voice_enabled']:
            success = agent.voice_commander.start_continuous_listening()
            if success:
                message = 'Voice commands enabled'
            else:
                agent_state['voice_enabled'] = False
                message = 'Failed to enable voice commands'
                return jsonify({'success': False, 'message': message, 'enabled': False}), 500
        else:
            agent.voice_commander.stop_listening()
            message = 'Voice commands disabled'
        
        return jsonify({'success': True, 'message': message, 'enabled': agent_state['voice_enabled']})
    except Exception as e:
        logger.error(f"Voice toggle error: {e}")
        agent_state['voice_enabled'] = False
        return jsonify({'success': False, 'error': str(e), 'enabled': False}), 500


@app.route('/api/gesture_stats', methods=['GET'])
def api_gesture_stats():
    """Get gesture detection statistics."""
    history = agent_state['gesture_history']
    
    if not history:
        return jsonify({
            'total_gestures': 0,
            'gesture_types': {},
            'average_confidence': 0.0
        })
    
    gesture_counts = {}
    total_confidence = 0
    
    for entry in history:
        gesture = entry.get('gesture', 'unknown')
        gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        total_confidence += entry.get('confidence', 0.0)
    
    return jsonify({
        'total_gestures': len(history),
        'gesture_types': gesture_counts,
        'average_confidence': total_confidence / len(history) if history else 0.0,
        'most_common': max(gesture_counts.items(), key=lambda x: x[1])[0] if gesture_counts else None
    })


@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'agent_initialized': agent is not None,
        'agent_running': agent_state['running']
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Gesture AI Agent Web Server")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
