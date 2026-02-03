"""
Demo script showing CRUD operations and action execution

This demonstrates how to use the ActionExecutor for various operations
"""

from action_executor import ActionExecutor

def main():
    print("=" * 60)
    print("GESTURE-BASED CRUD OPERATIONS DEMO")
    print("=" * 60)
    
    executor = ActionExecutor()
    
    # CREATE - Create a new note
    print("\n1. CREATE - Creating a new note...")
    result = executor.create_note("This is a test note created by gesture!")
    print(f"   Result: {result}")
    
    # READ - Read all notes
    print("\n2. READ - Reading all notes...")
    result = executor.read_notes()
    print(f"   Found {len(result.get('notes', []))} note(s)")
    
    # UPDATE - Update a note
    if result.get('notes'):
        filename = result['notes'][0]['file']
        print(f"\n3. UPDATE - Updating note: {filename}...")
        result = executor.update_note(filename, "Added more content via gesture!")
        print(f"   Result: {result}")
    
    # System Actions Demo
    print("\n" + "=" * 60)
    print("SYSTEM ACTIONS DEMO")
    print("=" * 60)
    
    print("\n4. Testing blink actions:")
    print("   - Single blink: Opens Camera")
    print("   - Double blink: Takes Screenshot")
    print("   - Triple blink: Opens Notepad")
    
    print("\n5. Testing mood-based actions:")
    print("   - Happy: Plays notification")
    print("   - Sad: Logs mood to file")
    print("   - Surprised: Captures screenshot")
    print("   - Angry: Clears notifications")
    
    # Show action history
    print("\n" + "=" * 60)
    print("ACTION HISTORY")
    print("=" * 60)
    history = executor.get_action_history()
    for i, action in enumerate(history, 1):
        print(f"{i}. {action['timestamp']}: {action['action_type']}")
    
    # Save log
    print("\n6. Saving action log...")
    result = executor.save_log_to_file()
    print(f"   Result: {result}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print("\nTo use these features in the main application:")
    print("1. Run: python main.py")
    print("2. Look at the camera")
    print("3. Blink patterns trigger different actions")
    print("4. Your facial expressions are detected automatically")
    print("5. Press 'h' to see action history")
    print("6. Press 'r' to reset blink counter")
    print("7. Press 'q' to quit")

if __name__ == "__main__":
    main()
