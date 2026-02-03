import pyttsx3
import json
import random
from datetime import datetime
import threading

class ConversationEngine:
    """Local conversation engine - no external API calls"""
    
    def __init__(self):
        # Initialize text-to-speech
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level
            self.speaking_enabled = False  # Disable speech to avoid errors
        except Exception as e:
            print(f"Warning: Text-to-speech initialization failed: {e}")
            self.engine = None
            self.speaking_enabled = False
        
        self.speech_lock = threading.Lock()  # Prevent multiple threads from speaking at once
        
        # Conversation memory
        self.conversation_history = []
        self.user_name = "Friend"
        self.context = {
            'time': self._get_time_of_day(),
            'mood': 'neutral'
        }
        
        # Response patterns based on gestures
        self.gesture_responses = {
            'thumbs_up': [
                "That's awesome! I love your enthusiasm!",
                "Great! You're doing amazing!",
                "Excellent gesture! Everything looks good!",
                "I appreciate the positive vibes!",
                "Perfect! You've got great energy!"
            ],
            'peace_sign': [
                "Peace to you too! Always good to see that gesture.",
                "Keep spreading the peace vibes!",
                "That's a classic one! Peace out!",
                "I like the peaceful energy you're sending!",
                "Two fingers for victory and peace!"
            ],
            'open_palm': [
                "An open hand - I see honesty and openness here!",
                "Open palms mean open heart!",
                "That's a welcoming gesture!",
                "I sense sincerity in that hand gesture!",
                "Beautiful open palm gesture!"
            ],
            'pointing': [
                "Pointing at something interesting?",
                "I see you're directing my attention!",
                "That's a strong pointing gesture!",
                "What are you pointing to?",
                "Directing the conversation, I see!"
            ],
            'raise_hand': [
                "You've raised your hand! Do you have a question?",
                "I see the raised hand - you have something to say!",
                "Got a question or comment for me?",
                "Your hand is raised - I'm listening!",
                "Raising your hand - let's hear it!"
            ],
            'wave': [
                "Hello! Nice to see you waving!",
                "A friendly wave! How are you doing?",
                "Wave back at you! Glad to see you!",
                "Waving is always a friendly gesture!",
                "Hey there! Nice wave!"
            ],
            'neutral': [
                "I'm here and listening!",
                "Still watching you!",
                "Ready for more gestures!",
                "What else can I help you with?",
                "I'm here whenever you need me!"
            ]
        }
    
    def generate_response(self, gesture_info):
        """Generate natural language response based on gesture"""
        gesture_type = gesture_info['gesture_type']
        confidence = gesture_info['confidence']
        
        # Select appropriate response list
        responses = self.gesture_responses.get(gesture_type, self.gesture_responses['neutral'])
        
        # Choose random response
        response = random.choice(responses)
        
        # Add context if confidence is very high
        if confidence > 0.85:
            response += " (Very clear gesture!)"
        
        # Store in history
        self.conversation_history.append({
            'gesture': gesture_type,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'confidence': confidence
        })
        
        return response
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.speaking_enabled or self.engine is None:
            return
        
        with self.speech_lock:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error speaking: {e}")
    
    def process_voice_command(self, voice_text):
        """Process voice commands (placeholder for future speech-to-text integration)"""
        voice_text = voice_text.lower()
        
        # Simple intent matching
        if 'hello' in voice_text or 'hi' in voice_text:
            return f"Hello {self.user_name}! How are you doing?"
        elif 'how are you' in voice_text:
            return "I'm doing great, thanks for asking! Ready to interact with your gestures."
        elif 'what time' in voice_text:
            return f"It's currently {datetime.now().strftime('%I:%M %p')}"
        elif 'help' in voice_text:
            return "I can recognize your gestures like thumbs up, peace sign, pointing, waving, raising your hand, and open palm. Just show me a gesture and I'll respond!"
        else:
            return "I understood you, but I need to improve my speech recognition. Try showing me a gesture instead!"
    
    def _get_time_of_day(self):
        """Get current time of day"""
        hour = datetime.now().hour
        if hour < 12:
            return "morning"
        elif hour < 17:
            return "afternoon"
        else:
            return "evening"
    
    def get_conversation_summary(self):
        """Get summary of conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        gesture_counts = {}
        for entry in self.conversation_history:
            gesture = entry['gesture']
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        summary = f"Conversation Summary:\n"
        summary += f"Total interactions: {len(self.conversation_history)}\n"
        summary += f"Gestures detected: {json.dumps(gesture_counts, indent=2)}\n"
        
        return summary
    
    def save_conversation(self, filename='conversation_log.json'):
        """Save conversation history to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            print(f"Conversation saved to {filename}")
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    def load_conversation(self, filename='conversation_log.json'):
        """Load conversation history from file"""
        try:
            with open(filename, 'r') as f:
                self.conversation_history = json.load(f)
            print(f"Conversation loaded from {filename}")
        except Exception as e:
            print(f"Error loading conversation: {e}")
