#!/usr/bin/env python3
"""
Test the current Android Studio launch implementation
"""

import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def test_android_studio_launch():
    """Test Android Studio launch with current implementation"""
    print("🧪 Testing Android Studio Launch Implementation")
    print("=" * 50)
    
    # HARDCODED Android Studio path (same as in app.py)
    studio_exe = r"C:\Program Files\Android\Android Studio\bin\studio64.exe"
    
    # Test project path (use current directory)
    test_project_path = os.path.abspath(".")
    
    print(f"📍 Studio path: {studio_exe}")
    print(f"📁 Test project: {test_project_path}")
    print(f"✅ Studio exists: {os.path.exists(studio_exe)}")
    
    if not os.path.exists(studio_exe):
        print("❌ Android Studio not found at hardcoded path!")
        return False
    
    print("\n🚀 Testing launch methods...")
    
    # Method 1: Direct launch with project path (same as app.py)
    print("\n1️⃣ Method 1: Direct launch with project")
    try:
        process = subprocess.Popen([studio_exe, test_project_path], shell=False)
        print(f"   ✅ SUCCESS: Process started with PID {process.pid}")
        
        # Wait a moment to see if it stays running
        import time
        time.sleep(2)
        
        if process.poll() is None:
            print("   ✅ Process still running - launch successful!")
            process.terminate()  # Clean up
            return True
        else:
            print(f"   ❌ Process exited with code: {process.returncode}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Method 2: Launch Android Studio only
    print("\n2️⃣ Method 2: Launch Android Studio only")
    try:
        process = subprocess.Popen([studio_exe], shell=False)
        print(f"   ✅ SUCCESS: Process started with PID {process.pid}")
        
        import time
        time.sleep(2)
        
        if process.poll() is None:
            print("   ✅ Process still running - launch successful!")
            process.terminate()  # Clean up
            return True
        else:
            print(f"   ❌ Process exited with code: {process.returncode}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Method 3: Shell launch
    print("\n3️⃣ Method 3: Shell launch")
    try:
        process = subprocess.Popen(f'"{studio_exe}" "{test_project_path}"', shell=True)
        print(f"   ✅ SUCCESS: Process started with PID {process.pid}")
        
        import time
        time.sleep(2)
        
        if process.poll() is None:
            print("   ✅ Process still running - launch successful!")
            process.terminate()  # Clean up
            return True
        else:
            print(f"   ❌ Process exited with code: {process.returncode}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    return False

if __name__ == "__main__":
    success = test_android_studio_launch()
    
    if success:
        print("\n🎉 Android Studio launch is working!")
        print("The issue might be elsewhere in the application.")
    else:
        print("\n❌ Android Studio launch failed!")
        print("Need to investigate further.")