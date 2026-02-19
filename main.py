import cv2
import numpy as np
import os
from gesture_processor import GestureProcessor
from conversation_engine import ConversationEngine
from facial_detector import FacialDetector
from action_executor import ActionExecutor
from voice_commander import VoiceCommander
from mood_music_player import MoodMusicPlayer
import threading
import time

# Try to import mediapipe - handle both old and new API
try:
    import mediapipe as mp
    if hasattr(mp, 'solutions'):
        # Old API
        mp_hands = mp.solutions.hands
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
    else:
        # New API - use tasks
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        mp_hands = None  # Will use new API
        mp_pose = None
        mp_drawing = None
    USE_MEDIAPIPE = True
except ImportError:
    USE_MEDIAPIPE = False
    print("MediaPipe not available, using simplified detection")

class GestureAIAgent:
    def __init__(self):
        # For now, use OpenCV-based detection since MediaPipe API changed
        self.use_mediapipe = False
        self.mp_drawing = None
        
        self.gesture_processor = GestureProcessor()
        self.conversation_engine = ConversationEngine()
        self.facial_detector = FacialDetector()
        self.action_executor = ActionExecutor()
        self.music_player = MoodMusicPlayer()
        
        # Initialize voice commander
        self.voice_commander = VoiceCommander(command_callback=self._handle_voice_command)
        self.voice_enabled = False
        # Register mood updates from facial detector to trigger mood actions (non-blocking)
        try:
            if hasattr(self.facial_detector, 'register_mood_callback') and hasattr(self.action_executor, 'execute_mood_action'):
                def _mood_cb(mood, confidence):
                    threading.Thread(target=self.action_executor.execute_mood_action, args=(mood, confidence), daemon=True).start()
                    # Also update music player
                    if self.music_player.available:
                        self.music_player.on_mood_detected(mood, confidence)
                self.facial_detector.register_mood_callback(_mood_cb)
        except Exception:
            pass
        # Register gesture callbacks to forward to ActionExecutor.handle_gesture
        try:
            if hasattr(self.gesture_processor, 'gesture_callbacks') and hasattr(self.action_executor, 'handle_gesture'):
                def _gesture_cb(gesture_type, info):
                    # Forward to action executor asynchronously
                    threading.Thread(target=self.action_executor.handle_gesture, args=(gesture_type,), daemon=True).start()
                # Prefer using a register method if available, otherwise append directly
                if hasattr(self.gesture_processor, 'register_gesture_callback'):
                    self.gesture_processor.register_gesture_callback(_gesture_cb)
                else:
                    self.gesture_processor.gesture_callbacks.append(_gesture_cb)
        except Exception:
            pass
        # Open camera with several fallbacks to avoid "device busy" issues
        self.cap = self._open_camera()
        if not self.cap or not self.cap.isOpened():
            print("Error: Unable to open a camera. Ensure no other app is using it and camera permissions are allowed.")
            self.running = False
            return

        # Set camera resolution
        try:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        except Exception:
            pass
        
        self.running = True
        self.current_gesture = None
        self.gesture_history = []
        
        # Stability improvements
        self.last_gesture_time = 0
        self.gesture_cooldown = 2.0  # Seconds between gesture responses
        self.frame_skip = 0
        self.process_every_n_frames = 2  # Process every nth frame for stability
        
        # Facial detection tracking
        self.last_blink_action_time = 0
        self.blink_cooldown = 3.0  # Seconds between blink actions
        self.last_mood_action_time = 0
        self.mood_cooldown = 5.0  # Seconds between mood-based actions
        
    def detect_gestures(self, frame):
        """Detect hand, body gestures, and facial features"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect facial features
        facial_features = self.facial_detector.detect_face_and_features(frame)
        blink_info = None
        expression_info = None
        
        if facial_features:
            blink_info = self.facial_detector.detect_blink(facial_features, frame)
            expression_info = self.facial_detector.detect_expression(facial_features, frame)
            
            # Draw facial info on frame
            frame = self.facial_detector.draw_info(frame, blink_info, expression_info)
        
        # Simple color-based hand detection (HSV skin tone)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create mask for skin color
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Apply morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on frame
        if contours:
            # Find largest contour (likely hand)
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 5000:  # Minimum area threshold
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                
                # Get convex hull for finger detection
                hull = cv2.convexHull(largest_contour)
                cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)
                
                # Count fingers using convexity defects
                hull_indices = cv2.convexHull(largest_contour, returnPoints=False)
                if len(hull_indices) > 3:
                    try:
                        defects = cv2.convexityDefects(largest_contour, hull_indices)
                        if defects is not None:
                            finger_count = 0
                            for i in range(defects.shape[0]):
                                s, e, f, d = defects[i, 0]
                                start = tuple(largest_contour[s][0])
                                end = tuple(largest_contour[e][0])
                                far = tuple(largest_contour[f][0])
                                
                                # Calculate angle
                                a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                                b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                                c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                                







                                # Avoid division by zero
                                if b * c > 0:
                                    angle = np.arccos(np.clip((b**2 + c**2 - a**2) / (2 * b * c), -1.0, 1.0))
                                    
                                    if angle <= np.pi / 2:  # Angle less than 90 degrees
                                        finger_count += 1
                                        cv2.circle(frame, far, 5, (0, 0, 255), -1)
                            
                            # Display finger count
                            cv2.putText(frame, f"Fingers: {finger_count}", (10, 90),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    except cv2.error:
                        # Skip if contour has self-intersections
                        pass
        
        # Create mock results for gesture processor
        pose_results = type('obj', (object,), {'pose_landmarks': None})()
        hand_results = type('obj', (object,), {
            'multi_hand_landmarks': [type('obj', (object,), {'landmark': self._create_mock_landmarks()})()]
            if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 5000 else []
        })()
        
        # Combine facial data
        facial_data = {
            'blink': blink_info,
            'expression': expression_info
        }
        
        return frame, pose_results, hand_results, facial_data

    def _open_camera(self):
        """Try multiple backends and device indices to open a camera on Windows reliably."""
        backends = []
        # Prefer DirectShow and Media Foundation on Windows
        try:
            backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        except Exception:
            backends = [cv2.CAP_ANY]

        for backend in backends:
            for idx in range(0, 4):
                try:
                    cap = cv2.VideoCapture(idx, backend)
                    # small delay to allow device to initialize
                    time.sleep(0.2)
                    if cap is not None and cap.isOpened():
                        print(f"Opened camera index={idx} backend={backend}")
                        return cap
                    else:
                        try:
                            cap.release()
                        except Exception:
                            pass
                except Exception:
                    continue

        return None
    
    def _create_mock_landmarks(self):
        """Create mock landmarks for gesture detection"""
        # Create 21 hand landmarks (MediaPipe standard)
        landmarks = []
        for i in range(21):
            landmark = type('obj', (object,), {
                'x': 0.5,
                'y': 0.5,
                'z': 0.0,
                'visibility': 1.0
            })()
            landmarks.append(landmark)
        return landmarks
    
    def draw_landmarks(self, frame, pose_results, hand_results):
        """Draw detected landmarks on frame"""
        # Landmarks are already drawn in detect_gestures
        return frame
    
    def process_gesture_and_respond(self, pose_results, hand_results, facial_data=None):
        """Process detected gesture and generate response with debouncing"""
        gesture_data = {
            'pose': pose_results,
            'hands': hand_results,
            'facial': facial_data,
            'timestamp': time.time()
        }
        
        gesture_info = self.gesture_processor.analyze_gesture(gesture_data)
        
        current_time = time.time()
        
        # Process blink actions
        blink_action_result = None
        if facial_data and facial_data.get('blink'):
            blink_info = facial_data['blink']
            if (blink_info['blink_detected'] and 
                blink_info['blink_type'] and
                current_time - self.last_blink_action_time >= self.blink_cooldown):
                
                blink_action_result = self.action_executor.execute_blink_action(blink_info['blink_type'])
                self.last_blink_action_time = current_time
                print(f"\n👁️ Blink Action: {blink_info['blink_type']} -> {blink_action_result}")
        
        # Process mood-based actions
        mood_action_result = None
        if facial_data and facial_data.get('expression'):
            expr_info = facial_data['expression']
            if (expr_info['mood'] != 'neutral' and 
                current_time - self.last_mood_action_time >= self.mood_cooldown):
                
                mood_action_result = self.action_executor.execute_mood_action(
                    expr_info['mood'], 
                    expr_info['confidence']
                )
                if mood_action_result:
                    self.last_mood_action_time = current_time
                    print(f"\n😊 Mood Action: {expr_info['mood']} -> {mood_action_result}")
        
        # Check if gesture is stable and confidence is high enough
        if (gesture_info and 
            gesture_info['confidence'] > 0.65 and 
            gesture_info.get('stable', False) and
            gesture_info['gesture_type'] != 'neutral'):
            
            # Check cooldown to prevent rapid repeated responses
            if current_time - self.last_gesture_time >= self.gesture_cooldown:
                self.current_gesture = gesture_info['gesture_type']
                self.gesture_history.append(gesture_info['gesture_type'])
                
                # Keep only last 10 gestures
                if len(self.gesture_history) > 10:
                    self.gesture_history.pop(0)
                
                # Generate response based on gesture
                response = self.conversation_engine.generate_response(gesture_info)
                
                # Update last gesture time
                self.last_gesture_time = current_time
                
                return response, gesture_info
        
        return None, gesture_info
    
    def run(self):
        """Main agent loop"""
        print("🤖 Gesture AI Agent Started")
        print("Features: Hand Gestures | Facial Expressions | Blink Detection | Voice Commands | Mood Music")
        print("Blink Actions: Single=WhatsApp | Double=Screenshot | Triple=Notepad")
        print("\nVoice Commands: 'open whatsapp', 'take screenshot', 'open notepad', 'open browser'")
        print("\nControls:")
        print("  'v' - Toggle continuous voice listening")
        print("  'l' - Listen for single voice command")
        print("  'm' - Toggle mood-based music auto-play")
        print("  'n' - Play next track")
        print("  'f' - Set custom music folder")
        print("  '+'/'-' - Volume up/down")
        print("  'p' - Pause/Resume music")
        print("  'q' - Quit")
        print("  'r' - Reset blink counter")
        print("  'h' - Show action history\n")
        
        # Check for custom music folder configuration
        music_config_file = 'music_config.txt'
        if os.path.exists(music_config_file):
            with open(music_config_file, 'r') as f:
                custom_folder = f.read().strip()
                if custom_folder and os.path.exists(custom_folder):
                    print(f"📁 Loading music from: {custom_folder}")
                    self.music_player.set_custom_music_folder(custom_folder)
        
        # Setup music library and enable auto-play
        if not self.music_player.use_custom_folder:
            self.music_player.setup_demo_music_library()
        
        self.music_player.set_auto_play(True)
        print("🎵 Mood-based music auto-play enabled!\n")
        
        while self.running:
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            # Flip frame for selfie view
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Frame skipping for more stable processing
            self.frame_skip += 1
            if self.frame_skip % self.process_every_n_frames != 0:
                cv2.imshow('Gesture AI Agent', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.running = False
                    print("\n👋 Shutting down agent...")
                    break
                continue
            
            # Detect gestures and facial features
            frame, pose_results, hand_results, facial_data = self.detect_gestures(frame)
            
            # Draw landmarks
            frame = self.draw_landmarks(frame, pose_results, hand_results)
            
            # Process gesture
            response, gesture_info = self.process_gesture_and_respond(pose_results, hand_results, facial_data)
            
            # Display information
            if gesture_info:
                stable_text = "[STABLE]" if gesture_info.get('stable', False) else "[DETECTING]"
                status_text = f"Gesture: {gesture_info['gesture_type']} | Conf: {gesture_info['confidence']:.2f} {stable_text}"
                color = (0, 255, 0) if gesture_info.get('stable', False) else (0, 165, 255)
                cv2.putText(frame, status_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Display voice command status
            voice_status = "Voice: ON" if self.voice_enabled else "Voice: OFF (press 'v')"
            voice_color = (0, 255, 0) if self.voice_enabled else (128, 128, 128)
            cv2.putText(frame, voice_status, (w - 250, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, voice_color, 2)
            
            # Display music player status
            music_status = "🎵 Music ON" if self.music_player.auto_play_enabled else "🎵 Music OFF (press 'm')"
            music_color = (100, 200, 255) if self.music_player.auto_play_enabled else (128, 128, 128)
            cv2.putText(frame, music_status, (w - 250, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, music_color, 1)
            
            if response:
                cv2.putText(frame, f"Agent: {response[:50]}...", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                print(f"🤖 Agent: {response}")
                # Speech is disabled to avoid threading errors
                # Uncomment below to enable speech (may cause errors)
                # threading.Thread(target=self.conversation_engine.speak, 
                #                args=(response,), daemon=True).start()
            
            # Show frame
            cv2.imshow('Gesture AI Agent', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
                print("\n👋 Shutting down agent...")
                break
            elif key == ord('r'):
                # Reset blink counter
                self.facial_detector.reset_blink_counter()
                print("\n🔄 Blink counter reset")
            elif key == ord('h'):
                # Show action history
                history = self.action_executor.get_action_history()
                print("\n📋 Recent Actions:")
                for action in history:
                    print(f"  - {action['timestamp']}: {action['action_type']}")
            elif key == ord('v'):
                # Toggle voice commands
                self._toggle_voice_commands()
            elif key == ord('l'):
                # Listen for single voice command
                print("\n🎤 Listening for voice command...")
                threading.Thread(target=self._listen_once, daemon=True).start()
            elif key == ord('m'):
                # Toggle music auto-play
                self.music_player.toggle_auto_play()
            elif key == ord('n'):
                # Next track
                if self.music_player.current_mood:
                    self.music_player.next_track()
                else:
                    print("🎵 Play a track first or auto-play must be enabled")
            elif key == ord('f'):
                # Set custom music folder
                print("\n📁 Enter your music folder path (or press Enter to skip):")
                print("Example: C:\\Users\\YourName\\Music\\MyPlaylist")
                # This will be set via config file for now
                print("💡 Create a file 'music_config.txt' with your music folder path and restart")
            elif key == ord('p'):
                # Pause/Resume
                if self.music_player.is_playing:
                    self.music_player.pause()
                else:
                    self.music_player.resume()
            elif key == ord('+') or key == ord('='):
                # Increase volume
                self.music_player.increase_volume()
            elif key == ord('-') or key == ord('_'):
                # Decrease volume
                self.music_player.decrease_volume()
        
        self.cleanup()
    
    def _handle_voice_command(self, command):
        """Handle voice command from VoiceCommander"""
        print(f"\n🎙️ Voice Command: '{command}'")
        result = self.action_executor.process_voice_command(command)
        if result:
            print(f"✅ Action: {result.get('action', result.get('message', 'Executed'))}")
    
    def _toggle_voice_commands(self):
        """Toggle continuous voice command listening"""
        if not self.voice_enabled:
            if self.voice_commander.start_listening():
                self.voice_enabled = True
                print("\n✅ Voice commands ENABLED - speak your commands!")
        else:
            self.voice_commander.stop_listening()
            self.voice_enabled = False
            print("\n🔇 Voice commands DISABLED")
    
    def _listen_once(self):
        """Listen for a single voice command"""
        command = self.voice_commander.listen_once()
        if command:
            self._handle_voice_command(command)
    
    def cleanup(self):
        """Clean up resources"""
        # Stop voice commander
        if hasattr(self, 'voice_commander') and self.voice_commander:
            self.voice_commander.stop_listening()
        
        # Stop music player
        if hasattr(self, 'music_player') and self.music_player:
            self.music_player.cleanup()
        
        try:
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
        except Exception as e:
            print(f"Error releasing camera: {e}")
        
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error closing windows: {e}")

if __name__ == "__main__":
    agent = GestureAIAgent()
    agent.run()
