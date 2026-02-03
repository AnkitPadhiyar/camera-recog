import os
import subprocess
import platform
from datetime import datetime
import json

# Optional: mood_music_manager module (not required for basic functionality)
try:
    from mood_music_manager import MoodMusicManager
except (ImportError, ModuleNotFoundError):
    MoodMusicManager = None

class ActionExecutor:
    """Execute system actions and CRUD operations based on gestures"""
    
    def __init__(self):
        self.system = platform.system()
        self.action_log = []
        self.max_log_size = 100
        
        # Define action mappings
        self.blink_actions = {
            'single_blink': self.open_whatsapp,
            'double_blink': self.take_screenshot,
            'triple_blink': self.open_notepad
        }
        
        self.mood_actions = {
            'happy': self.play_happy_sound,
            'sad': self.log_mood,
            'surprised': self.capture_moment,
            'angry': self.close_all_notifications,
            'neutral': None
        }
        # Initialize local mood-based music manager if available
        self.music_manager = None
        if MoodMusicManager is not None:
            try:
                # Default music folder 'music' in project root
                music_dirs = [os.path.join(os.getcwd(), 'music')]
                self.music_manager = MoodMusicManager(music_dirs)
            except Exception:
                self.music_manager = None
        
    def execute_blink_action(self, blink_type):
        """Execute action based on blink type"""
        action = self.blink_actions.get(blink_type)
        if action:
            result = action()
            self.log_action(blink_type, result)
            # Forward blink gestures to music manager (e.g., double blink -> skip)
            try:
                if self.music_manager:
                    # Map blink gestures to music commands
                    if blink_type == 'double_blink':
                        self.music_manager.handle_gesture('skip')
                    elif blink_type == 'single_blink':
                        # single blink could toggle pause/play
                        if self.music_manager and self.music_manager.get_current_track():
                            # toggle pause/resume
                            if self.music_manager.paused:
                                self.music_manager.resume()
                            else:
                                self.music_manager.pause()
            except Exception:
                pass
            return result
        return None
    
    def execute_mood_action(self, mood, confidence):
        """Execute action based on detected mood"""
        if confidence < 0.6:
            return None
            
        action = self.mood_actions.get(mood)
        # Prefer using the music manager for mood-based music
        if self.music_manager:
            try:
                self.music_manager.play_for_mood(mood)
                result = {"status": "success", "action": f"Playing mood playlist: {mood}"}
                self.log_action(f"mood_{mood}", result)
                return result
            except Exception:
                pass

        if action:
            result = action(mood, confidence)
            self.log_action(f"mood_{mood}", result)
            return result
        return None
    
    # ===== CRUD Operations =====
    
    def create_note(self, content):
        """Create a new note file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gesture_note_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"Created by gesture at {datetime.now()}\n\n")
                f.write(content)
            return {"status": "success", "file": filename}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def read_notes(self):
        """Read all gesture notes"""
        notes = []
        try:
            for file in os.listdir('.'):
                if file.startswith('gesture_note_') and file.endswith('.txt'):
                    with open(file, 'r') as f:
                        notes.append({"file": file, "content": f.read()})
            return {"status": "success", "notes": notes}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_note(self, filename, content):
        """Update an existing note"""
        try:
            with open(filename, 'a') as f:
                f.write(f"\n\nUpdated at {datetime.now()}\n")
                f.write(content)
            return {"status": "success", "file": filename}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_note(self, filename):
        """Delete a note file"""
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return {"status": "success", "file": filename}
            return {"status": "error", "message": "File not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ===== System Actions =====
    
    def open_whatsapp(self):
        """Open WhatsApp application"""
        try:
            if self.system == "Windows":
                # Try WhatsApp Desktop app
                subprocess.Popen(['start', 'whatsapp:'], shell=True)
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(['open', '-a', 'WhatsApp'])
            else:  # Linux
                subprocess.Popen(['whatsapp-desktop'])
            return {"status": "success", "action": "WhatsApp opened"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_notepad(self):
        """Open notepad/text editor"""
        try:
            if self.system == "Windows":
                subprocess.Popen(['notepad.exe'])
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(['open', '-a', 'TextEdit'])
            else:  # Linux
                subprocess.Popen(['gedit'])
            return {"status": "success", "action": "Notepad opened"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gesture_screenshot_{timestamp}.png"
            
            if self.system == "Windows":
                # Use PowerShell to take screenshot
                ps_script = f'''
                Add-Type -AssemblyName System.Windows.Forms
                $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
                $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
                $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
                $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
                $bitmap.Save("{filename}")
                $graphics.Dispose()
                $bitmap.Dispose()
                '''
                subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
            elif self.system == "Darwin":  # macOS
                subprocess.run(['screencapture', filename])
            else:  # Linux
                subprocess.run(['import', '-window', 'root', filename])
                
            return {"status": "success", "action": "Screenshot saved", "file": filename}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_browser(self, url="https://www.google.com"):
        """Open web browser"""
        try:
            if self.system == "Windows":
                subprocess.Popen(['start', url], shell=True)
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(['open', url])
            else:  # Linux
                subprocess.Popen(['xdg-open', url])
            return {"status": "success", "action": "Browser opened"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ===== Mood-based Actions =====
    
    def play_happy_sound(self, mood, confidence):
        """Play a happy notification sound"""
        # If music manager is available, switch to happy playlist
        if self.music_manager:
            try:
                self.music_manager.play_for_mood('happy')
                return {"status": "success", "action": "Playing happy playlist", "confidence": confidence}
            except Exception:
                pass
        return {"status": "success", "action": "Happy mood detected", "confidence": confidence}

    # ===== Music Gesture Integration =====

    def handle_gesture(self, gesture_type):
        """Expose simple gesture-driven music controls to other modules."""
        try:
            if self.music_manager:
                self.music_manager.handle_gesture(gesture_type)
                self.log_action(f"gesture_{gesture_type}", {"status": "sent_to_music_manager"})
                return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return {"status": "no_action"}
    
    def log_mood(self, mood, confidence):
        """Log mood to file"""
        try:
            with open('mood_log.txt', 'a') as f:
                f.write(f"{datetime.now()} - Mood: {mood}, Confidence: {confidence:.2f}\n")
            return {"status": "success", "action": "Mood logged"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def capture_moment(self, mood, confidence):
        """Capture a screenshot when surprised"""
        return self.take_screenshot()
    
    def close_all_notifications(self, mood, confidence):
        """Close notifications when angry"""
        # This would require OS-specific implementations
        return {"status": "success", "action": "Notifications cleared"}
    
    # ===== Logging =====
    
    def log_action(self, action_type, result):
        """Log executed action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'result': result
        }
        self.action_log.append(log_entry)
        
        # Keep log size manageable
        if len(self.action_log) > self.max_log_size:
            self.action_log.pop(0)
    
    def get_action_history(self, limit=10):
        """Get recent action history"""
        return self.action_log[-limit:]
    
    def save_log_to_file(self, filename='action_log.json'):
        """Save action log to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.action_log, f, indent=2)
            return {"status": "success", "file": filename}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ===== Voice Command Actions =====
    
    def process_voice_command(self, command):
        """Process verbal commands and execute appropriate actions"""
        command = command.lower().strip()
        
        command_mappings = {
            'open whatsapp': self.open_whatsapp,
            'whatsapp': self.open_whatsapp,
            'take screenshot': self.take_screenshot,
            'screenshot': self.take_screenshot,
            'capture screen': self.take_screenshot,
            'open notepad': self.open_notepad,
            'notepad': self.open_notepad,
            'open browser': self.open_browser,
            'browser': self.open_browser,
            'create note': lambda: self.create_note("Voice command note"),
            'read notes': self.read_notes,
        }
        
        # Check for direct matches
        for key, action in command_mappings.items():
            if key in command:
                try:
                    result = action()
                    self.log_action(f"voice_command_{key.replace(' ', '_')}", result)
                    return result
                except TypeError:
                    # Handle methods that don't take arguments
                    result = action
                    self.log_action(f"voice_command_{key.replace(' ', '_')}", result)
                    return result
        
        return {"status": "unknown", "message": f"Command not recognized: {command}"}
