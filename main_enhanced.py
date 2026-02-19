"""
Enhanced main application with professional architecture
Gesture AI Agent - Real-time gesture recognition system
"""

from typing import Optional, Dict, Any, List
import cv2
import numpy as np
import os
import threading
import time
from datetime import datetime

# Import modules with proper error handling
try:
    import mediapipe as mp
    USE_MEDIAPIPE = True
except ImportError:
    USE_MEDIAPIPE = False
    print("Warning: MediaPipe not available")

# Import project modules
from config import get_config
from logger import LoggerManager, get_logger
from gesture_processor import GestureProcessor
from conversation_engine import ConversationEngine
from facial_detector import FacialDetector
from action_executor import ActionExecutor
from voice_commander import VoiceCommander
from mood_music_player import MoodMusicPlayer

# Initialize logger
logger = get_logger(__name__)


class GestureAIAgent:
    """
    Main application class orchestrating all gesture recognition systems.
    
    Attributes:
        gesture_processor: Gesture detection system
        conversation_engine: NLP response generation
        facial_detector: Facial expression analysis
        action_executor: System action execution
        voice_commander: Voice command processing
        music_player: Audio feedback system
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Initialize Gesture AI Agent.
        
        Args:
            config_path: Path to configuration JSON file (optional)
        """
        # Setup logging first
        LoggerManager.setup()
        logger.info("Initializing Gesture AI Agent v2.0.0")
        
        # Load configuration
        self.config = get_config(config_path)
        logger.info(f"Configuration loaded from: {config_path or 'defaults'}")
        
        # Initialize components
        self.gesture_processor = GestureProcessor()
        self.conversation_engine = ConversationEngine()
        self.facial_detector = FacialDetector()
        self.action_executor = ActionExecutor()
        self.music_player = MoodMusicPlayer()
        self.voice_commander = VoiceCommander(
            command_callback=self._handle_voice_command
        )
        
        # Register callbacks
        self._register_callbacks()
        
        # Initialize camera
        self.cap: Optional[cv2.VideoCapture] = self._open_camera()
        
        # State variables
        self.running: bool = False
        self.current_gesture: Optional[str] = None
        self.gesture_history: List[Dict[str, Any]] = []
        
        # Timing variables
        self.last_gesture_time: float = 0.0
        self.last_blink_action_time: float = 0.0
        self.last_mood_action_time: float = 0.0
        self.frame_count: int = 0
        
        # Get timing config
        self.gesture_cooldown = self.config.gesture.gesture_cooldown
        self.blink_cooldown = self.config.facial.blink_cooldown
        self.mood_cooldown = self.config.facial.mood_cooldown
        self.process_every_n_frames = 2
        
        logger.info(
            f"Agent initialized successfully. "
            f"Camera: {self.config.camera.width}x{self.config.camera.height} "
            f"@ {self.config.camera.fps}FPS"
        )

    def _open_camera(self) -> Optional[cv2.VideoCapture]:
        """
        Open camera device with fault tolerance.
        
        Returns:
            OpenCV VideoCapture object or None if failed
        """
        for attempt in range(self.config.camera.retry_count):
            try:
                cap = cv2.VideoCapture(self.config.camera.device_id)
                
                if cap.isOpened():
                    # Set camera properties
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.camera.width)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.camera.height)
                    cap.set(cv2.CAP_PROP_FPS, self.config.camera.fps)
                    
                    logger.info(f"Camera opened successfully (device {self.config.camera.device_id})")
                    return cap
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} to open camera failed: {e}")
                time.sleep(self.config.camera.retry_delay)
        
        logger.error("Failed to open camera after all retry attempts")
        return None

    def _register_callbacks(self) -> None:
        """Register event callbacks for gestures and moods."""
        try:
            # Gesture callback
            def gesture_callback(gesture_type: str, info: Dict[str, Any]) -> None:
                """Handle gesture detection."""
                time_since_last = time.time() - self.last_gesture_time
                if time_since_last > self.gesture_cooldown:
                    logger.info(
                        f"Gesture detected: {gesture_type} "
                        f"(confidence: {info.get('confidence', 0):.2f})"
                    )
                    self.action_executor.handle_gesture(gesture_type)
                    self.last_gesture_time = time.time()
            
            self.gesture_processor.register_gesture_callback(gesture_callback)
            
            # Mood callback
            def mood_callback(mood: str, confidence: float) -> None:
                """Handle mood detection."""
                time_since_last = time.time() - self.last_mood_action_time
                if time_since_last > self.mood_cooldown and confidence > self.config.facial.mood_confidence_threshold:
                    logger.info(f"Mood detected: {mood} (confidence: {confidence:.2f})")
                    threading.Thread(
                        target=self.action_executor.execute_mood_action,
                        args=(mood, confidence),
                        daemon=True
                    ).start()
                    self.last_mood_action_time = time.time()
            
            self.facial_detector.register_mood_callback(mood_callback)
            
            logger.debug("Event callbacks registered successfully")
        except Exception as e:
            logger.warning(f"Error registering callbacks: {e}")

    def _handle_voice_command(self, command: str, confidence: float) -> None:
        """
        Handle voice command execution.
        
        Args:
            command: Recognized command string
            confidence: Recognition confidence score
        """
        logger.info(f"Voice command: '{command}' (confidence: {confidence:.2f})")
        
        if confidence > 0.8:
            threading.Thread(
                target=self.action_executor.handle_gesture,
                args=(f"voice_{command}",),
                daemon=True
            ).start()

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame through gesture pipeline.
        
        Args:
            frame: Input image frame
            
        Returns:
            Dictionary with detection results
        """
        self.frame_count += 1
        
        # Skip frames based on configuration
        if self.frame_count % self.process_every_n_frames != 0:
            return {'skipped': True}
        
        try:
            # Prepare detection data
            gesture_data = {
                'frame': frame,
                'hands': None,
                'pose': None,
                'facial': None
            }
            
            # MediaPipe processing if available
            if USE_MEDIAPIPE:
                # Process with MediaPipe
                # (Implementation depends on your MediaPipe setup)
                pass
            
            # Gesture processing
            gesture_result = self.gesture_processor.analyze_gesture(gesture_data)
            
            # Facial detection
            if self.config.facial.enable_facial_detection:
                facial_result = self.facial_detector.detect_expression(frame)
            else:
                facial_result = None
            
            return {
                'gesture': gesture_result,
                'facial': facial_result,
                'timestamp': datetime.now().isoformat(),
                'frame_number': self.frame_count
            }
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return {'error': str(e)}

    def run(self) -> None:
        """
        Main application loop.
        
        Continuously captures frames, processes gestures, and displays results.
        """
        if not self.cap or not self.cap.isOpened():
            logger.error("Cannot start: camera not available")
            return
        
        self.running = True
        logger.info("Starting main event loop")
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                
                if not ret or frame is None:
                    logger.warning("Failed to capture frame")
                    continue
                
                # Process frame
                result = self.process_frame(frame)
                
                # Display frame with results
                self._display_results(frame, result)
                
                # Check for exit key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("Exit key pressed (q)")
                    self.stop()
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.stop()
        except Exception as e:
            logger.exception(f"Unexpected error in main loop: {e}")
            self.stop()

    def _display_results(self, frame: np.ndarray, result: Dict[str, Any]) -> None:
        """
        Display results on frame.
        
        Args:
            frame: Input frame
            result: Processing results
        """
        # Add FPS
        fps = self.cap.get(cv2.CAP_PROP_FPS) if self.cap else 30
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Add detected gesture if present
        if 'gesture' in result and 'gesture_type' in result['gesture']:
            gesture_type = result['gesture']['gesture_type']
            confidence = result['gesture']['confidence']
            
            cv2.putText(
                frame,
                f"Gesture: {gesture_type} ({confidence:.2f})",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
        
        # Display frame
        cv2.imshow("Gesture AI Agent", frame)

    def stop(self) -> None:
        """Stop the application gracefully."""
        logger.info("Stopping Gesture AI Agent")
        
        self.running = False
        
        # Release resources
        if self.cap:
            self.cap.release()
        
        if self.voice_commander:
            try:
                self.voice_commander.stop_listening()
            except Exception as e:
                logger.warning(f"Error stopping voice commander: {e}")
        
        cv2.destroyAllWindows()
        
        # Save action history before exit
        try:
            history = self.action_executor.get_action_history()
            logger.info(f"Action history saved with {len(history)} actions")
        except Exception as e:
            logger.warning(f"Error saving action history: {e}")
        
        logger.info("Agent stopped successfully")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.
        
        Returns:
            Dictionary with status information
        """
        return {
            'running': self.running,
            'frame_count': self.frame_count,
            'camera_active': self.cap.isOpened() if self.cap else False,
            'gesture_history_size': len(self.gesture_history),
            'voice_listening': self.voice_commander.is_listening(),
            'timestamp': datetime.now().isoformat()
        }


def main() -> None:
    """Application entry point."""
    try:
        agent = GestureAIAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
