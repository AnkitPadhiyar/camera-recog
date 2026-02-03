import speech_recognition as sr
import threading
import time
from queue import Queue

class VoiceCommander:
    """Handle voice command recognition and processing"""
    
    def __init__(self, command_callback=None):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.command_callback = command_callback
        self.command_queue = Queue()
        self.listen_thread = None
        self.microphone_available = False
        
        # Adjust recognition settings
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Initialize microphone with better error handling
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                print("🎤 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Microphone ready!")
                self.microphone_available = True
        except Exception as e:
            print(f"⚠️ Microphone initialization failed: {e}")
            print("⚠️ Voice commands will be disabled. Other features (gestures, facial detection) will continue to work.")
            self.microphone = None
            self.microphone_available = False
    
    def start_listening(self):
        """Start listening for voice commands in background"""
        if not self.microphone_available:
            print("❌ Microphone not available - voice commands disabled")
            return False
        
        if self.is_listening:
            print("Already listening...")
            return True
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        print("🎤 Voice command listening started!")
        return True
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("🔇 Voice command listening stopped")
    
    def _listen_loop(self):
        """Main listening loop (runs in background thread)"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    print("🎤 Listening for command...")
                    
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    try:
                        # Recognize speech using Google Speech Recognition
                        print("🔄 Processing speech...")
                        command = self.recognizer.recognize_google(audio)
                        print(f"✅ Recognized: '{command}'")
                        
                        # Add to queue and trigger callback
                        self.command_queue.put(command)
                        if self.command_callback:
                            self.command_callback(command)
                        
                    except sr.UnknownValueError:
                        print("❓ Could not understand audio")
                    except sr.RequestError as e:
                        print(f"❌ Recognition service error: {e}")
                    
            except sr.WaitTimeoutError:
                # Timeout is normal, just continue listening
                pass
            except Exception as e:
                print(f"⚠️ Listening error: {e}")
                time.sleep(1)
    
    def get_command(self, block=False, timeout=None):
        """Get next command from queue"""
        try:
            return self.command_queue.get(block=block, timeout=timeout)
        except:
            return None
    
    def listen_once(self):
        """Listen for a single command (blocking)"""
        if not self.microphone:
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening for command...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                
                try:
                    command = self.recognizer.recognize_google(audio)
                    print(f"✅ Recognized: '{command}'")
                    return command
                except sr.UnknownValueError:
                    print("❓ Could not understand audio")
                    return None
                except sr.RequestError as e:
                    print(f"❌ Recognition service error: {e}")
                    return None
        except sr.WaitTimeoutError:
            print("⏱️ Listening timeout")
            return None
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return None
    
    def test_microphone(self):
        """Test if microphone is working"""
        if not self.microphone:
            return False
        
        try:
            with self.microphone as source:
                print("🎤 Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio)
                print(f"✅ Test successful! Heard: '{text}'")
                return True
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False
