#!/usr/bin/env python3
"""
Web UI Setup Verification Script
Checks if all dependencies are installed and working correctly
"""

import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print(f"{Colors.BOLD}Checking Python Version...{Colors.RESET}")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"{Colors.GREEN}✓ Python {version.major}.{version.minor}.{version.micro} ✓{Colors.RESET}")
        return True
    else:
        print(f"{Colors.RED}✗ Python {version.major}.{version.minor} is too old (need 3.8+) ✗{Colors.RESET}")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"{Colors.GREEN}✓ {package_name} is installed ✓{Colors.RESET}")
        return True
    except ImportError:
        print(f"{Colors.RED}✗ {package_name} is NOT installed ✗{Colors.RESET}")
        return False

def check_file_exists(filepath):
    """Check if a required file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"{Colors.GREEN}✓ {filepath} found ✓{Colors.RESET}")
        return True
    else:
        print(f"{Colors.RED}✗ {filepath} NOT found ✗{Colors.RESET}")
        return False

def check_camera():
    """Check if camera is accessible"""
    print(f"{Colors.BOLD}Checking Camera Access...{Colors.RESET}")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print(f"{Colors.GREEN}✓ Camera is working ✓{Colors.RESET}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠ Camera found but cannot read frames ⚠{Colors.RESET}")
                return False
        else:
            print(f"{Colors.YELLOW}⚠ Camera not found or not accessible ⚠{Colors.RESET}")
            return False
    except Exception as e:
        print(f"{Colors.YELLOW}⚠ Camera check error: {str(e)} ⚠{Colors.RESET}")
        return False

def main():
    print_header("Web UI Setup Verification")
    
    all_ok = True
    
    # Check Python version
    print(f"{Colors.BOLD}1. Python Version{Colors.RESET}")
    all_ok = check_python_version() and all_ok
    
    # Check required files
    print(f"\n{Colors.BOLD}2. Required Files{Colors.RESET}")
    required_files = [
        'app.py',
        'config.py',
        'main_enhanced.py',
        'templates/index.html',
        'static/style.css',
        'static/app.js',
        'requirements.txt',
        'requirements-web.txt'
    ]
    
    for file in required_files:
        if not check_file_exists(file):
            all_ok = False
    
    # Check core dependencies
    print(f"\n{Colors.BOLD}3. Core Dependencies (main project){Colors.RESET}")
    core_packages = [
        ('OpenCV', 'cv2'),
        ('NumPy', 'numpy'),
        ('MediaPipe', 'mediapipe'),
    ]
    
    for package_name, import_name in core_packages:
        if not check_package(package_name, import_name):
            all_ok = False
    
    # Check web dependencies
    print(f"\n{Colors.BOLD}4. Web Dependencies{Colors.RESET}")
    web_packages = [
        ('Flask', 'flask'),
        ('Flask-CORS', 'flask_cors'),
    ]
    
    for package_name, import_name in web_packages:
        if not check_package(package_name, import_name):
            print(f"{Colors.YELLOW}  → Run: pip install -r requirements-web.txt{Colors.RESET}")
            all_ok = False
    
    # Check optional dependencies
    print(f"\n{Colors.BOLD}5. Optional Dependencies{Colors.RESET}")
    optional_packages = [
        ('SpeechRecognition', 'speech_recognition'),
        ('pyttsx3', 'pyttsx3'),
        ('sounddevice', 'sounddevice'),
        ('Pillow', 'PIL'),
    ]
    
    for package_name, import_name in optional_packages:
        try:
            __import__(import_name)
            print(f"{Colors.GREEN}✓ {package_name} is installed ✓{Colors.RESET}")
        except ImportError:
            print(f"{Colors.YELLOW}⚠ {package_name} is missing (optional) ⚠{Colors.RESET}")
    
    # Check camera
    check_camera()
    
    # Summary
    print_header("Verification Summary")
    
    if all_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed! You're ready to start the web UI!{Colors.RESET}\n")
        print(f"{Colors.BOLD}Next steps:{Colors.RESET}")
        print(f"  1. Run the web server:")
        print(f"     python app.py")
        print(f"\n  2. Open your browser:")
        print(f"     http://localhost:5000\n")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ Some issues found. Please install missing dependencies:{Colors.RESET}\n")
        print(f"{Colors.BOLD}Install missing dependencies:{Colors.RESET}")
        print(f"  pip install -r requirements.txt")
        print(f"  pip install -r requirements-web.txt\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
