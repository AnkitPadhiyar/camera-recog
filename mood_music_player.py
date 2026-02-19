import os
import random
import threading
from collections import defaultdict
import json
from pathlib import Path
import subprocess
import platform

class MoodMusicPlayer:
    """Play mood-appropriate music based on detected facial expressions"""
    
    def __init__(self):
        try:
            self.system = platform.system()
            print("🎵 Music player initialized successfully!")
            self.available = True
            self.music_process = None
        except Exception as e:
            print(f"⚠️ Failed to initialize music player: {e}")
            self.available = False
            return
        self.current_track = None
        self.is_playing = False
        self.current_mood = None
        self.auto_play_enabled = False
        self.music_volume = 0.5
        
        # Music library - can be mood-specific or from custom folder
        self.use_custom_folder = False
        self.custom_music_folder = None
        self.all_music_files = []
        
        # Music library organized by mood (default/fallback)
        self.music_library = {
            'happy': [],
            'sad': [],
            'surprised': [],
            'angry': [],
            'neutral': []
        }
        
        # Track play history to avoid repetition
        self.recent_tracks = defaultdict(list)
        self.mood_change_count = 0
        
    def set_custom_music_folder(self, folder_path):
        """Set a custom music folder to use your existing playlist"""
        if not os.path.exists(folder_path):
            print(f"❌ Folder not found: {folder_path}")
            return False
        
        self.custom_music_folder = folder_path
        print(f"📁 Scanning music folder: {folder_path}")
        
        # Scan for audio files
        audio_extensions = ('.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma', '.aac')
        self.all_music_files = []
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(audio_extensions):
                        full_path = os.path.join(root, file)
                        self.all_music_files.append({
                            'path': full_path,
                            'name': file,
                            'folder': os.path.basename(root)
                        })
            
            if len(self.all_music_files) > 0:
                self.use_custom_folder = True
                print(f"✅ Found {len(self.all_music_files)} music files!")
                print(f"🎵 Your playlist is now connected!")
                
                # Distribute songs across moods for variety
                self._distribute_songs_to_moods()
                return True
            else:
                print(f"⚠️ No audio files found in {folder_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error scanning folder: {e}")
            return False
    
    def _distribute_songs_to_moods(self):
        """Distribute all songs across moods for random selection"""
        # Clear existing libraries
        for mood in self.music_library:
            self.music_library[mood] = []
        
        # Add all songs to all moods (mixed genre approach)
        # This way any song can play for any mood
        for song in self.all_music_files:
            for mood in self.music_library:
                self.music_library[mood].append(song)
        
    def set_auto_play(self, enabled):
        """Enable/disable automatic music playing"""
        self.auto_play_enabled = enabled
        if enabled:
            print("🎵 Auto-play enabled - music will play based on your mood!")
        else:
            print("🎵 Auto-play disabled")
    
    def toggle_auto_play(self):
        """Toggle auto-play mode"""
        self.set_auto_play(not self.auto_play_enabled)
        return self.auto_play_enabled
    
    def on_mood_detected(self, mood, confidence):
        """Called when a new mood is detected"""
        if not self.available or not self.auto_play_enabled:
            return
        
        # Only change music if mood confidence is high enough
        if confidence < 0.5:
            return
        
        # If mood changed significantly, play new music
        if self.current_mood != mood:
            self.mood_change_count += 1
            self.current_mood = mood
            self._play_mood_music(mood)
    
    def _play_mood_music(self, mood):
        """Select and play a track for the given mood"""
        if mood not in self.music_library:
            mood = 'neutral'
        
        # Get available tracks for this mood
        available_tracks = self.music_library[mood]
        if not available_tracks:
            print(f"⚠️ No tracks available for mood: {mood}")
            return
        
        # Prefer tracks not recently played
        if self.use_custom_folder:
            # For custom folder, track by file path
            recent = set([t['path'] if isinstance(t, dict) else t for t in self.recent_tracks[mood]])
            new_tracks = [t for t in available_tracks if (t['path'] if isinstance(t, dict) else t) not in recent]
        else:
            recent = set(self.recent_tracks[mood])
            new_tracks = [t for t in available_tracks if t not in recent]
        
        # If all tracks were recent, clear history and use all
        if not new_tracks:
            self.recent_tracks[mood].clear()
            new_tracks = available_tracks
        
        # Select random track
        selected_track = random.choice(new_tracks)
        self.recent_tracks[mood].append(selected_track)
        
        # Keep only last 5 tracks in history
        if len(self.recent_tracks[mood]) > 5:
            self.recent_tracks[mood].pop(0)
        
        # Play the track
        if isinstance(selected_track, dict):
            self.play_track(selected_track['path'], mood, display_name=selected_track['name'])
        else:
            self.play_track(selected_track, mood)
    
    def play_track(self, track_name, mood=None, display_name=None):
        """Play a specific track"""
        if not self.available:
            print("⚠️ Music player not available")
            return False
        
        # Use display name if provided, otherwise use track_name
        display = display_name if display_name else os.path.basename(track_name)
        
        try:
            print(f"🎵 Now playing: {display} ({mood if mood else 'custom'})")
            self.current_track = display
            self.is_playing = True
            
            # Determine music path
            if self.use_custom_folder and os.path.exists(track_name):
                music_path = track_name
            else:
                music_path = self._get_music_path(track_name)
            
            if os.path.exists(music_path):
                try:
                    # Stop any currently playing music
                    self.stop()
                    
                    # Play music using system default player
                    if self.system == 'Windows':
                        # Use Windows Media Player in background
                        self.music_process = subprocess.Popen(
                            ['powershell', '-c', f'(New-Object Media.SoundPlayer "{music_path}").PlaySync()'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    elif self.system == 'Darwin':  # macOS
                        self.music_process = subprocess.Popen(
                            ['afplay', music_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    else:  # Linux
                        self.music_process = subprocess.Popen(
                            ['mpg123', '-q', music_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    
                    print(f"✅ Playing: {display}")
                    return True
                except Exception as e:
                    print(f"⚠️ Could not play audio file: {e}")
                    return False
            else:
                print(f"💡 Music file not found: {music_path}")
                if not self.use_custom_folder:
                    print(f"💡 Tip: Use set_custom_music_folder() to connect your playlist")
                return False
                
        except Exception as e:
            print(f"❌ Error playing track: {e}")
            return False
    
    def _get_music_path(self, track_name):
        """Get full path to music file"""
        mood_folder = self.current_mood or 'neutral'
        return os.path.join('music_library', mood_folder, track_name)
    
    def pause(self):
        """Pause current playback"""
        if self.available and self.is_playing:
            print("⏸️  Music paused (stop/start to control playback)")
            # Note: Simple process control doesn't support pause/resume easily
            return True
        return False
    
    def resume(self):
        """Resume playback"""
        if self.available and not self.is_playing:
            print("▶️  Music resumed (restart track)")
            return True
        return False
    
    def stop(self):
        """Stop playback"""
        if self.available and self.music_process:
            try:
                self.music_process.terminate()
                self.music_process.wait(timeout=2)
                self.is_playing = False
                self.current_track = None
                print("⏹️  Music stopped")
                return True
            except Exception as e:
                print(f"❌ Error stopping: {e}")
                # Force kill if needed
                try:
                    self.music_process.kill()
                except:
                    pass
        return False
    
    def next_track(self):
        """Skip to next track for current mood"""
        if self.current_mood:
            self._play_mood_music(self.current_mood)
            return True
        return False
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        self.music_volume = volume
        print(f"🔊 Volume set to {int(volume*100)}%")
        # Note: Volume control requires platform-specific commands
        return True
    
    def increase_volume(self):
        """Increase volume by 10%"""
        self.set_volume(self.music_volume + 0.1)
    
    def decrease_volume(self):
        """Decrease volume by 10%"""
        self.set_volume(self.music_volume - 0.1)
    
    def get_status(self):
        """Get current player status"""
        return {
            'available': self.available,
            'playing': self.is_playing,
            'current_track': self.current_track,
            'current_mood': self.current_mood,
            'auto_play': self.auto_play_enabled,
            'volume': int(self.music_volume * 100),
            'mood_changes': self.mood_change_count
        }
    
    def get_mood_tracks(self, mood):
        """Get all tracks available for a mood"""
        return self.music_library.get(mood, [])
    
    def setup_demo_music_library(self):
        """Create demo music library structure (without actual files)"""
        print("\n📁 Setting up music library structure...")
        
        base_path = 'music_library'
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        for mood, tracks in self.music_library.items():
            mood_path = os.path.join(base_path, mood)
            if not os.path.exists(mood_path):
                os.makedirs(mood_path)
                print(f"  ✅ Created: {mood_path}/")
        
        # Create README with setup instructions
        readme_path = os.path.join(base_path, 'README.md')
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("""# Music Library Setup

## How to Add Your Music

1. Download or create MP3 files for each mood
2. Organize them in mood-specific folders:
   - `music_library/happy/` - Upbeat, energetic songs
   - `music_library/sad/` - Calm, soothing songs
   - `music_library/surprised/` - Exciting, dramatic songs
   - `music_library/angry/` - Intense, powerful songs
   - `music_library/neutral/` - Background, ambient songs

3. Name files exactly as shown in the application

## Supported Formats
- MP3 (recommended)
- WAV
- OGG
- FLAC

## Example Structure
```
music_library/
├── happy/
│   ├── upbeat_joy.mp3
│   ├── cheerful_morning.mp3
│   └── ...
├── sad/
│   ├── calm_reflection.mp3
│   └── ...
└── neutral/
    └── ambient_background.mp3
```

The player will automatically select from available files in each mood folder!
""")
            print(f"  ✅ Created: {readme_path}")
        
        print("✅ Music library ready! Add MP3 files to start playing mood-based music.\n")
    
    def handle_gesture(self, gesture_type):
        """Handle gesture-based music controls"""
        gesture_map = {
            'wave': self.next_track,
            'thumbs_up': lambda: self.increase_volume(),
            'open_palm': lambda: self.pause() if self.is_playing else self.resume(),
            'pointing': lambda: self.decrease_volume(),
        }
        
        handler = gesture_map.get(gesture_type)
        if handler:
            try:
                handler()
                return True
            except Exception as e:
                print(f"Error handling gesture {gesture_type}: {e}")
        return False
    
    def cleanup(self):
        """Clean up music player"""
        try:
            if self.available:
                self.stop()
        except:
            pass
