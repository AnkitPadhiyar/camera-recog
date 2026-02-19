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
    'last_action': None,
    'last_action_time': None,
    'voice_enabled': False,
    'frame_count': 0,
    'gesture_history': [],
    'action_history': []
}

current_frame = None
frame_lock = threading.Lock()


def init_agent():
    """Initialize the gesture AI agent."""
    global agent
    try:
        if agent is None:
            agent = GestureAIAgent()
            logger.info("Gesture AI Agent initialized")
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
            
            # Process frame - only every nth frame for performance
            agent.frame_count += 1
            if agent.frame_count % agent.process_every_n_frames == 0:
                try:
                    # Detect facial features
                    facial_features = agent.facial_detector.detect_face_and_features(frame)
                    blink_info = None
                    expression_info = None
                    
                    if facial_features:
                        blink_info = agent.facial_detector.detect_blink(facial_features, frame)
                        expression_info = agent.facial_detector.detect_expression(facial_features, frame)
                    
                    # Combine facial data
                    facial_data = {
                        'blink': blink_info,
                        'expression': expression_info
                    }
                    
                    # Process gesture using the facial data
                    gesture_data = {
                        'pose': None,
                        'hands': None,
                        'facial': facial_data,
                        'timestamp': time.time()
                    }
                    
                    gesture_info = agent.gesture_processor.analyze_gesture(gesture_data)
                    
                    # Update gesture state
                    if gesture_info and gesture_info.get('gesture_type') != 'neutral':
                        gesture = gesture_info['gesture_type']
                        confidence = gesture_info.get('confidence', 0.0)
                        
                        if gesture != agent.current_gesture and confidence > 0.6:
                            agent.current_gesture = gesture
                            agent_state['current_gesture'] = gesture
                            agent_state['gesture_confidence'] = confidence
                            agent_state['last_action'] = gesture
                            agent_state['last_action_time'] = datetime.now().isoformat()
                            
                            logger.info(f"Gesture detected: {gesture} (confidence: {confidence:.2f})")
                            
                            # Add to history
                            agent_state['gesture_history'].append({
                                'gesture': gesture,
                                'confidence': confidence,
                                'timestamp': agent_state['last_action_time']
                            })
                            
                            # Keep only last 50 entries
                            if len(agent_state['gesture_history']) > 50:
                                agent_state['gesture_history'].pop(0)
                    else:
                        agent.current_gesture = None
                        agent_state['current_gesture'] = None
                        agent_state['gesture_confidence'] = 0.0
                    
                    # Update emotion state from expression
                    if expression_info and expression_info.get('mood'):
                        emotion = expression_info['mood']
                        confidence = expression_info.get('confidence', 0.0)
                        
                        agent_state['current_emotion'] = emotion
                        agent_state['emotion_confidence'] = confidence
                        
                        logger.debug(f"Emotion detected: {emotion} (confidence: {confidence:.2f})")
                    else:
                        agent_state['current_emotion'] = None
                        agent_state['emotion_confidence'] = 0.0
                    
                    # Process blinks
                    if blink_info and blink_info.get('blink_detected'):
                        agent_state['last_action'] = f"Blink ({blink_info.get('blink_type', 'single')})"
                        agent_state['last_action_time'] = datetime.now().isoformat()
                        logger.debug(f"Blink detected: {blink_info.get('blink_type')}")
                
                except AttributeError as e:
                    logger.error(f"Component method missing: {e}")
                except Exception as e:
                    logger.error(f"Frame processing error: {e}")
            
            # Put text on frame for displaying status
            emotion_text = agent_state['current_emotion'] or 'None'
            gesture_text = agent_state['current_gesture'] or 'None'
            
            cv2.putText(frame, f"Gesture: {gesture_text}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Emotion: {emotion_text}", 
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


@app.route('/api/voice/toggle', methods=['POST'])
def api_voice_toggle():
    """Toggle voice command recognition."""
    if agent is None:
        return jsonify({'success': False, 'error': 'Agent not initialized'}), 400
    
    try:
        agent_state['voice_enabled'] = not agent_state['voice_enabled']
        
        if agent_state['voice_enabled']:
            agent.voice_commander.start_continuous_listening()
            message = 'Voice commands enabled'
        else:
            agent.voice_commander.stop_listening()
            message = 'Voice commands disabled'
        
        return jsonify({'success': True, 'message': message, 'enabled': agent_state['voice_enabled']})
    except Exception as e:
        logger.error(f"Voice toggle error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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
