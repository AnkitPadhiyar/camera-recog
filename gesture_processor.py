import numpy as np
import math

class GestureProcessor:
    """Process and classify detected gestures"""
    
    def __init__(self):
        self.gesture_thresholds = {
            'raise_hand': 0.65,  # Lowered from 0.7
            'wave': 0.70,        # Lowered from 0.75
            'thumbs_up': 0.75,   # Lowered from 0.8
            'peace_sign': 0.80,  # Lowered from 0.85
            'point': 0.65,       # Lowered from 0.7
            'open_palm': 0.70,   # Lowered from 0.75
            'face_detected': 0.4  # New: confidence for just facial features
        }
        
        # Stability improvements
        self.gesture_buffer = []  # Store recent gesture detections
        self.buffer_size = 5  # Number of frames to consider
        self.last_confirmed_gesture = None
        self.gesture_hold_frames = 0
        self.min_hold_frames = 2  # Lowered from 3 for faster response
        self.confidence_history = []
        # Gesture callbacks: fn(gesture_type:str, info:dict)
        self.gesture_callbacks = []
    
    def register_gesture_callback(self, callback):
        """Register a callback function to be called when a gesture is detected"""
        if callable(callback):
            self.gesture_callbacks.append(callback)
    
    def analyze_gesture(self, gesture_data):
        """Analyze gesture data and classify with temporal smoothing"""
        pose = gesture_data['pose']
        hands = gesture_data['hands']
        facial = gesture_data.get('facial', None)  # Facial data (blink, expression)
        
        gesture_info = {
            'gesture_type': 'neutral',
            'confidence': 0.0,
            'details': {},
            'facial_data': None
        }
        
        # Analyze hand gestures FIRST (higher priority)
        if hands is not None:
            # Check if this is MediaPipe hand detection results
            if hasattr(hands, 'multi_hand_landmarks') and hands.multi_hand_landmarks:
                hand_gesture = self._analyze_hand_gesture(hands)
                if hand_gesture and hand_gesture['confidence'] > 0.5:
                    gesture_info = hand_gesture
        
        # Analyze body gestures
        if pose and hasattr(pose, 'pose_landmarks') and pose.pose_landmarks:
            body_gesture = self._analyze_body_gesture(pose)
            if body_gesture and body_gesture['confidence'] > gesture_info['confidence']:
                gesture_info = body_gesture
        
        # CRITICAL: Use facial expression data if no hand/pose gestures detected
        if facial and gesture_info.get('confidence', 0) < 0.5:
            gesture_info['facial_data'] = facial
            expression = facial.get('expression', None)
            
            # If we detected an expression, use it as the gesture with confidence
            if expression and expression.get('expression'):
                expression_type = expression['expression']
                expression_confidence = expression.get('confidence', 0.0)
                
                # Only update if expression has meaningful confidence
                if expression_confidence > 0.4:
                    gesture_info['gesture_type'] = expression_type
                    gesture_info['confidence'] = expression_confidence
                    gesture_info['details'] = {
                        'type': 'facial_expression',
                        'expression': expression_type,
                        'confidence': expression_confidence
                    }
        
        # Apply temporal smoothing
        gesture_info = self._smooth_gesture(gesture_info)
        
        return gesture_info
        return gesture_info
    
    def _analyze_hand_gesture(self, hands):
        """Analyze hand landmarks for gestures"""
        for hand_landmarks in hands.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            
            # Extract key points
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            ring_tip = landmarks[16]
            pinky_tip = landmarks[20]
            palm = landmarks[0]
            
            # Thumbs up gesture
            thumbs_up = self._is_thumbs_up(landmarks)
            if thumbs_up['confidence'] > 0.7:
                return {
                    'gesture_type': 'thumbs_up',
                    'confidence': thumbs_up['confidence'],
                    'details': thumbs_up
                }
            
            # Peace sign (V shape)
            peace = self._is_peace_sign(landmarks)
            if peace['confidence'] > 0.7:
                return {
                    'gesture_type': 'peace_sign',
                    'confidence': peace['confidence'],
                    'details': peace
                }
            
            # Open palm
            open_palm = self._is_open_palm(landmarks)
            if open_palm['confidence'] > 0.75:
                return {
                    'gesture_type': 'open_palm',
                    'confidence': open_palm['confidence'],
                    'details': open_palm
                }
            
            # Pointing gesture
            pointing = self._is_pointing(landmarks)
            if pointing['confidence'] > 0.7:
                return {
                    'gesture_type': 'pointing',
                    'confidence': pointing['confidence'],
                    'details': pointing
                }
        
        return {
            'gesture_type': 'neutral',
            'confidence': 0.0,
            'details': {}
        }
    
    def _analyze_body_gesture(self, pose):
        """Analyze body pose for gestures"""
        landmarks = pose.pose_landmarks.landmark
        
        # Key body points
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_elbow = landmarks[13]
        right_elbow = landmarks[14]
        left_hand = landmarks[15]
        right_hand = landmarks[16]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        
        # Raise hand gesture
        if (left_hand.y < left_shoulder.y and left_hand.confidence > 0.5) or \
           (right_hand.y < right_shoulder.y and right_hand.confidence > 0.5):
            return {
                'gesture_type': 'raise_hand',
                'confidence': 0.75,
                'details': {'raised_hand': 'left' if left_hand.y < left_shoulder.y else 'right'}
            }
        
        # Wave gesture (detect arm motion would need tracking)
        return {
            'gesture_type': 'neutral',
            'confidence': 0.0,
            'details': {}
        }
    
    def _is_thumbs_up(self, landmarks):
        """Detect thumbs up gesture"""
        thumb_ip = landmarks[2]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        
        # Thumb should be extended upward
        thumb_distance = abs(thumb_tip.y - thumb_ip.y)
        
        # Other fingers should be curled (lower y position than thumb)
        fingers_curled = (index_tip.y > thumb_tip.y and 
                         middle_tip.y > thumb_tip.y)
        
        confidence = thumb_distance * 0.5 if fingers_curled else 0.0
        
        return {
            'confidence': min(confidence, 1.0),
            'thumb_extended': thumb_distance > 0.05,
            'fingers_curled': fingers_curled
        }
    
    def _is_peace_sign(self, landmarks):
        """Detect peace sign (V shape)"""
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Index and middle should be extended and apart
        index_middle_distance = abs(index_tip.x - middle_tip.x)
        
        # Ring and pinky should be curled
        ring_curled = ring_tip.y > middle_tip.y
        pinky_curled = pinky_tip.y > middle_tip.y
        
        confidence = index_middle_distance * 0.7 if (ring_curled and pinky_curled) else 0.0
        
        return {
            'confidence': min(confidence, 1.0),
            'index_middle_distance': index_middle_distance,
            'fingers_curled': ring_curled and pinky_curled
        }
    
    def _is_open_palm(self, landmarks):
        """Detect open palm gesture"""
        # All fingertips should have similar y position (extended)
        fingertips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]]
        
        y_values = [tip.y for tip in fingertips]
        y_variance = np.var(y_values)
        
        # All fingers extended
        palm = landmarks[0]
        fingers_extended = all(tip.y < palm.y + 0.1 for tip in fingertips)
        
        confidence = 1.0 - (y_variance * 5) if fingers_extended else 0.0
        
        return {
            'confidence': min(max(confidence, 0.0), 1.0),
            'fingers_extended': fingers_extended,
            'variance': y_variance
        }
    
    def _is_pointing(self, landmarks):
        """Detect pointing gesture"""
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Index should be extended (higher than pip)
        index_extended = index_tip.y < index_pip.y - 0.05
        
        # Other fingers should be curled
        others_curled = (middle_tip.y > index_pip.y and 
                        ring_tip.y > index_pip.y and 
                        pinky_tip.y > index_pip.y)
        
        confidence = 0.8 if (index_extended and others_curled) else 0.0
        
        return {
            'confidence': confidence,
            'index_extended': index_extended,
            'others_curled': others_curled
        }
    
    def _smooth_gesture(self, gesture_info):
        """Apply temporal smoothing to reduce jitter and false detections"""
        # Add current gesture to buffer
        self.gesture_buffer.append(gesture_info)
        self.confidence_history.append(gesture_info['confidence'])
        
        # Keep buffer at fixed size
        if len(self.gesture_buffer) > self.buffer_size:
            self.gesture_buffer.pop(0)
            self.confidence_history.pop(0)
        
        # If buffer not full yet, return current gesture
        if len(self.gesture_buffer) < self.buffer_size:
            return gesture_info
        
        # Count gesture occurrences in buffer
        gesture_counts = {}
        for g in self.gesture_buffer:
            g_type = g['gesture_type']
            gesture_counts[g_type] = gesture_counts.get(g_type, 0) + 1
        
        # Find most common gesture
        most_common = max(gesture_counts.items(), key=lambda x: x[1])
        most_common_gesture = most_common[0]
        occurrence_ratio = most_common[1] / len(self.gesture_buffer)
        
        # Average confidence for the most common gesture
        avg_confidence = np.mean([
            g['confidence'] for g in self.gesture_buffer 
            if g['gesture_type'] == most_common_gesture
        ])
        
        # Gesture must appear in at least 60% of buffer frames
        if occurrence_ratio >= 0.6 and avg_confidence > 0.5:
            # Check if this is the same as last confirmed gesture
            if self.last_confirmed_gesture == most_common_gesture:
                self.gesture_hold_frames += 1
            else:
                # New gesture detected, start counting
                self.gesture_hold_frames = 1
            
            # Only confirm gesture after minimum hold frames
            if self.gesture_hold_frames >= self.min_hold_frames:
                self.last_confirmed_gesture = most_common_gesture
                result = {
                    'gesture_type': most_common_gesture,
                    'confidence': avg_confidence,
                    'details': gesture_info['details'],
                    'stable': True
                }
                # Notify callbacks about confirmed gesture
                try:
                    for cb in self.gesture_callbacks:
                        try:
                            cb(result['gesture_type'], result)
                        except Exception:
                            pass
                except Exception:
                    pass
                return result
        
        # Not stable enough, return neutral or last confirmed
        if self.last_confirmed_gesture and self.gesture_hold_frames > 0:
            # Gradually decay the last gesture
            self.gesture_hold_frames = max(0, self.gesture_hold_frames - 1)
            if self.gesture_hold_frames > 0:
                return {
                    'gesture_type': self.last_confirmed_gesture,
                    'confidence': avg_confidence * 0.8,
                    'details': gesture_info['details'],
                    'stable': False
                }
        
        return {
            'gesture_type': 'neutral',
            'confidence': 0.0,
            'details': {},
            'stable': False
        }
