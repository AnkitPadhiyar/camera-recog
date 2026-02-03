"""
Quick test script for voice commands
Run this to test voice recognition before using the main app
"""

from voice_commander import VoiceCommander
from action_executor import ActionExecutor
import time

def main():
    print("=" * 60)
    print("VOICE COMMAND TEST")
    print("=" * 60)
    print()
    
    # Initialize
    print("Initializing voice commander...")
    vc = VoiceCommander()
    executor = ActionExecutor()
    
    if not vc.microphone:
        print("❌ No microphone detected!")
        print("Please check your microphone connection and permissions.")
        return
    
    print("✅ Voice commander initialized!")
    print()
    
    # Test microphone
    print("=" * 60)
    print("MICROPHONE TEST")
    print("=" * 60)
    input("Press Enter to test your microphone...")
    
    success = vc.test_microphone()
    if not success:
        print("⚠️ Microphone test failed. Check your setup.")
        return
    
    print()
    
    # Test voice commands
    print("=" * 60)
    print("VOICE COMMAND TEST")
    print("=" * 60)
    print()
    print("Available commands:")
    print("  - 'open whatsapp'")
    print("  - 'take screenshot'")
    print("  - 'open notepad'")
    print("  - 'open browser'")
    print("  - 'create note'")
    print()
    
    for i in range(3):
        print(f"\nTest {i+1}/3")
        input("Press Enter to speak a command...")
        
        command = vc.listen_once()
        if command:
            print(f"✅ Recognized: '{command}'")
            result = executor.process_voice_command(command)
            print(f"📋 Result: {result}")
        else:
            print("❌ No command recognized")
        
        time.sleep(1)
    
    print()
    print("=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
    print()
    print("✅ If tests passed, you're ready to use voice commands!")
    print("Run: python main.py")
    print("Then press 'v' to enable voice commands")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install SpeechRecognition PyAudio")
        print("2. Check microphone permissions")
        print("3. Ensure internet connection (for Google Speech Recognition)")
