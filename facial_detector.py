import cv2
import numpy as np
import time
from collections import deque

class FacialDetector:
    """Detect facial features including blinks and expressions"""
    
    def __init__(self):
        # Load Haar Cascades for face and eye detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.eye_glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        # Blink detection parameters
        self.eye_ar_threshold = 0.25  # Eye aspect ratio threshold for blink
        self.blink_frames_threshold = 2  # Consecutive frames for blink
        
        self.left_eye_closed_frames = 0
        self.right_eye_closed_frames = 0
        self.both_eyes_closed_frames = 0
        
        self.blink_count = 0
        self.last_blink_time = 0
        self.blink_buffer = deque(maxlen=10)  # Track recent blinks
        
        # Glasses detection
        self.wearing_glasses = False
        self.glasses_frames = 0
        self.no_glasses_frames = 0
        
        # Expression detection parameters
        self.expression_history = deque(maxlen=5)
        self.last_expression = 'neutral'
        # Callbacks to notify on mood/expression updates
        self.mood_callbacks = []
        
        # Face tracking
        self.face_detected = False
        self.face_region = None
        
    def detect_face_and_features(self, frame):
        """Detect face and extract features"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            self.face_detected = False
            return None
        
        self.face_detected = True
        
        # Use the largest face
        face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = face
        self.face_region = (x, y, w, h)
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
        
        # Extract face ROI
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect eyes in face region (try without glasses first)
        eyes = self.eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(20, 20)
        )
        
        # If no eyes detected, try glasses cascade
        eyes_with_glasses = self.eye_glasses_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(20, 20)
        )
        
        # Determine glasses status
        if len(eyes_with_glasses) > 0 and len(eyes) == 0:
            self.glasses_frames += 1
            self.no_glasses_frames = 0
            if self.glasses_frames > 5:  # Confirm glasses for 5 frames
                self.wearing_glasses = True
        elif len(eyes) > 0:
            self.no_glasses_frames += 1
            self.glasses_frames = 0
            if self.no_glasses_frames > 5:  # Confirm no glasses for 5 frames
                self.wearing_glasses = False
        
        # Use whichever eyes were detected (glasses cascade if available)
        if len(eyes) == 0 and len(eyes_with_glasses) > 0:
            eyes = eyes_with_glasses
        
        # Detect smile
        smiles = self.smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.7,
            minNeighbors=22,
            minSize=(25, 25)
        )
        
        return {
            'face': face,
            'eyes': eyes,
            'smiles': smiles,
            'roi_gray': roi_gray,
            'roi_color': roi_color
        }
    
    def detect_blink(self, features, frame):
        """Detect eye blinks (works with or without glasses)"""
        if not features or not self.face_detected:
            return None
        
        if 'eyes' not in features or 'face' not in features:
            return None
        
        eyes = features['eyes']
        x, y, w, h = features['face']
        
        # Validate face region
        if w <= 0 or h <= 0:
            return None
        
        roi_color = features.get('roi_color')
        if roi_color is None:
            return None
        
        # Draw eyes (if detected)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        current_time = time.time()
        
        # Blink detection
        if self.wearing_glasses:
            # For glasses: use mouth region brightness as proxy for blink
            # (eyes hidden by glasses, but eye closure affects lighting)
            roi_gray = features.get('roi_gray')
            if roi_gray is not None:
                eye_region = roi_gray[0:int(h*0.4), :]
                eye_brightness = np.mean(eye_region)
                
                # Lower brightness = eyes might be closed
                if eye_brightness < 80:
                    self.both_eyes_closed_frames += 1
                else:
                    if self.both_eyes_closed_frames >= self.blink_frames_threshold:
                        self.blink_count += 1
                        self.blink_buffer.append(current_time)
                        self.last_blink_time = current_time
                        blink_type = self._analyze_blink_pattern(current_time)
                        self.both_eyes_closed_frames = 0
                        
                        return {
                            'blink_detected': True,
                            'blink_type': blink_type,
                            'blink_count': self.blink_count,
                            'confidence': 0.6,
                            'method': 'brightness_based'
                        }
                    self.both_eyes_closed_frames = 0
        else:
            # Normal eye detection without glasses
            if len(eyes) == 0:  # Both eyes closed
                self.both_eyes_closed_frames += 1
            else:
                if self.both_eyes_closed_frames >= self.blink_frames_threshold:
                    # Blink detected
                    self.blink_count += 1
                    self.blink_buffer.append(current_time)
                    self.last_blink_time = current_time
                    
                    # Determine blink pattern
                    blink_type = self._analyze_blink_pattern(current_time)
                    
                    self.both_eyes_closed_frames = 0
                    
                    return {
                        'blink_detected': True,
                        'blink_type': blink_type,
                        'blink_count': self.blink_count,
                        'confidence': 0.8,
                        'method': 'eye_detection'
                    }
                
                self.both_eyes_closed_frames = 0
        
        return {
            'blink_detected': False,
            'blink_type': None,
            'blink_count': self.blink_count,
            'confidence': 0.0
        }
    
    def _analyze_blink_pattern(self, current_time):
        """Analyze blink pattern (single, double, triple)"""
        recent_blinks = [t for t in self.blink_buffer if current_time - t < 1.5]
        
        if len(recent_blinks) >= 3:
            return 'triple_blink'
        elif len(recent_blinks) >= 2:
            return 'double_blink'
        else:
            return 'single_blink'
    
    def detect_expression(self, features, frame):
        """Detect facial expression and mood"""
        if not features or not self.face_detected:
            return None
        
        if 'face' not in features:
            return None
        
        x, y, w, h = features['face']
        
        # Validate face region
        if w <= 0 or h <= 0:
            return None
        
        smiles = features.get('smiles', [])
        eyes = features.get('eyes', [])
        roi_gray = features.get('roi_gray')
        
        if roi_gray is None:
            return None
        
        # Initialize expression scores with higher baseline for sensitivity
        expression_scores = {
            'happy': 0.1,
            'sad': 0.1,
            'surprised': 0.1,
            'angry': 0.1,
            'neutral': 0.6
        }
        
        # Happy detection (smile) - increased sensitivity
        if len(smiles) > 0:
            expression_scores['happy'] = 0.75 + (len(smiles) * 0.15)
            expression_scores['neutral'] = 0.2
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(features['roi_color'], (sx, sy), (sx+sw, sy+sh), (0, 255, 255), 2)
        
        # Enhanced facial region analysis for better expression detection
        if h > 0 and w > 0:
            # Eyebrow region (top 25% of face)
            eyebrow_region = roi_gray[0:int(h*0.25), :]
            eyebrow_mean = np.mean(eyebrow_region)
            eyebrow_std = np.std(eyebrow_region)
            
            # Mouth region (bottom 35% of face)
            mouth_region = roi_gray[int(h*0.65):h, :]
            mouth_mean = np.mean(mouth_region)
            mouth_std = np.std(mouth_region)
            
            # Eye region (top-middle 40%)
            eye_region = roi_gray[0:int(h*0.4), :]
            eye_mean = np.mean(eye_region)
            eye_std = np.std(eye_region)
            
            # No smile detected - analyze other features
            if len(smiles) == 0:
                # Angry: dark eyebrows + high mouth contrast (lowered threshold for sensitivity)
                if eyebrow_mean < 110 and eyebrow_std > 20 and mouth_std > 30:
                    expression_scores['angry'] = 0.65
                    expression_scores['happy'] = 0.1
                    expression_scores['neutral'] = 0.25
                
                # Sad: lighter eyebrows + lower mouth mean (lowered threshold)
                elif mouth_mean > 125 and eyebrow_mean > 95:
                    expression_scores['sad'] = 0.65
                    expression_scores['happy'] = 0.1
                    expression_scores['neutral'] = 0.25
                
                # Neutral: average values (improved baseline)
                else:
                    expression_scores['neutral'] = 0.65
                    expression_scores['happy'] = 0.15
            else:
                # Smiling reduces sad/angry scores
                expression_scores['sad'] = max(0.0, expression_scores['sad'] - 0.4)
                expression_scores['angry'] = max(0.0, expression_scores['angry'] - 0.4)
            
            # Surprise: wide eyes + minimal smile (improved detection)
            if len(eyes) >= 2 and len(smiles) == 0:
                eye_areas = [ew * eh for (ex, ey, ew, eh) in eyes]
                avg_eye_area = np.mean(eye_areas)
                # Lowered threshold for better sensitivity
                if avg_eye_area > 500 and eye_std > 25:
                    if eye_mean < 125:  # Bright eyes indicate openness
                        expression_scores['surprised'] = 0.70
                        expression_scores['neutral'] = 0.2
        
        # Get dominant expression
        dominant_expression = max(expression_scores.items(), key=lambda x: x[1])
        expression_type = dominant_expression[0]
        confidence = dominant_expression[1]
        
        # Ensure minimum confidence of 0.5 for detected faces
        confidence = max(0.5, confidence)
        
        # Add to history for smoothing
        self.expression_history.append((expression_type, confidence))
        
        # Get most common expression from history (less strict smoothing for responsiveness)
        if len(self.expression_history) >= 2:
            expr_counts = {}
            for expr, conf in self.expression_history:
                if expr not in expr_counts:
                    expr_counts[expr] = []
                expr_counts[expr].append(conf)
            
            # Get expression with highest average confidence
            avg_confidences = {expr: np.mean(confs) for expr, confs in expr_counts.items()}
            smoothed_expression = max(avg_confidences.items(), key=lambda x: x[1])
            expression_type = smoothed_expression[0]
            confidence = smoothed_expression[1]
        
        self.last_expression = expression_type

        # Notify callbacks about mood update
        try:
            if confidence >= 0.4:  # Lowered from 0.5 for sensitivity
                for cb in self.mood_callbacks:
                    try:
                        cb(expression_type, float(confidence))
                    except Exception:
                        pass
        except Exception:
            pass
        
        return {
            'expression': expression_type,
            'confidence': confidence,
            'all_scores': expression_scores,
            'mood': expression_type  # Map expression to mood
        }
    
    def draw_info(self, frame, blink_info, expression_info):
        """Draw detection information on frame"""
        y_offset = 120
        
        if self.face_detected:
            cv2.putText(frame, "Face: DETECTED", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Face: NOT DETECTED", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        y_offset += 30
        
        # Show glasses status
        glasses_status = "DETECTED 👓" if self.wearing_glasses else "NOT DETECTED"
        glasses_color = (200, 100, 255) if self.wearing_glasses else (200, 200, 200)
        cv2.putText(frame, f"Glasses: {glasses_status}", (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, glasses_color, 2)
        
        y_offset += 30
        
        if blink_info:
            blink_text = f"Blinks: {blink_info['blink_count']} | Last: {blink_info['blink_type']}"
            color = (255, 255, 0) if blink_info['blink_detected'] else (200, 200, 200)
            cv2.putText(frame, blink_text, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        y_offset += 30
        
        if expression_info:
            mood_text = f"Mood: {expression_info['mood'].upper()} ({expression_info['confidence']:.2f})"
            mood_colors = {
                'happy': (0, 255, 255),
                'sad': (255, 100, 100),
                'surprised': (255, 200, 0),
                'angry': (0, 0, 255),
                'neutral': (200, 200, 200)
            }
            color = mood_colors.get(expression_info['mood'], (255, 255, 255))
            cv2.putText(frame, mood_text, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def reset_blink_counter(self):
        """Reset blink counter"""
        self.blink_count = 0
        self.blink_buffer.clear()

    def register_mood_callback(self, fn):
        """Register a callback to receive mood updates: fn(mood:str, confidence:float)"""
        if callable(fn):
            self.mood_callbacks.append(fn)
