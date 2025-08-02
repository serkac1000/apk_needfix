#!/usr/bin/env python3
"""
Test Android Studio Launch - Debug auto-launch issues
This script helps identify why Android Studio isn't launching automatically
"""

import os
import subprocess
import glob

def find_android_studio():
    """Find Android Studio installation"""
    print("🔍 Searching for Android Studio installation...")
    
    username = os.getenv('USERNAME', '')
    android_studio_paths = [
        r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
        r"C:\Program Files (x86)\Android\Android Studio\bin\studio64.exe",
        rf"C:\Users\{username}\AppData\Local\Android\Studio\bin\studio64.exe",
        rf"C:\Users\{username}\AppData\Roaming\JetBrains\Toolbox\apps\AndroidStudio\ch-0\*\bin\studio64.exe",
        r"C:\Android\Android Studio\bin\studio64.exe",
        "studio64.exe",  # If in PATH
        "studio.exe"     # Alternative name
    ]

    found_paths = []
    
    for path in android_studio_paths:
        print(f"  Checking: {path}")
        
        if '*' in path:
            # Handle wildcard paths (like Toolbox installations)
            matches = glob.glob(path)
            if matches:
                for match in matches:
                    if os.path.exists(match):
                        found_paths.append(match)
                        print(f"    ✅ Found: {match}")
        elif os.path.exists(path):
            found_paths.append(path)
            print(f"    ✅ Found: {path}")
        else:
            print(f"    ❌ Not found")
    
    return found_paths

def test_launch_methods(studio_exe, test_project_path):
    """Test different launch methods"""
    print(f"\n🧪 Testing launch methods with: {studio_exe}")
    
    methods = [
        {
            'name': 'Method 1: Direct launch with project',
            'command': [studio_exe, test_project_path],
            'shell': False
        },
        {
            'name': 'Method 2: Launch Android Studio only',
            'command': [studio_exe],
            'shell': False
        },
        {
            'name': 'Method 3: Shell launch with quotes',
            'command': f'"{studio_exe}" "{test_project_path}"',
            'shell': True
        },
        {
            'name': 'Method 4: Shell launch without project',
            'command': f'"{studio_exe}"',
            'shell': True
        }
    ]
    
    for method in methods:
        print(f"\n  Testing: {method['name']}")
        try:
            if method['shell']:
                process = subprocess.Popen(method['command'], shell=True)
            else:
                process = subprocess.Popen(method['command'], shell=False)
            
            print(f"    ✅ SUCCESS: Process started with PID {process.pid}")
            print(f"    ⏳ Waiting 3 seconds to check if process is still running...")
            
            import time
            time.sleep(3)
            
            if process.poll() is None:
                print(f"    ✅ Process still running - launch successful!")
                process.terminate()  # Clean up test process
                return True
            else:
                print(f"    ❌ Process exited with code: {process.returncode}")
                
        except Exception as e:
            print(f"    ❌ FAILED: {e}")
    
    return False

def main():
    """Main test function"""
    print("🚀 Android Studio Launch Test")
    print("=" * 50)
    
    # Find Android Studio
    found_paths = find_android_studio()
    
    if not found_paths:
        print("\n❌ No Android Studio installation found!")
        print("\n💡 Possible solutions:")
        print("   1. Install Android Studio from https://developer.android.com/studio")
        print("   2. Add Android Studio to your PATH environment variable")
        print("   3. Check if Android Studio is installed in a custom location")
        return
    
    print(f"\n✅ Found {len(found_paths)} Android Studio installation(s)")
    
    # Use first found installation
    studio_exe = found_paths[0]
    print(f"\n🎯 Using: {studio_exe}")
    
    # Create a test project path (use current directory)
    test_project_path = os.path.abspath(".")
    print(f"📁 Test project path: {test_project_path}")
    
    # Test launch methods
    success = test_launch_methods(studio_exe, test_project_path)
    
    if success:
        print(f"\n🎉 SUCCESS: Android Studio can be launched automatically!")
        print(f"📝 Recommended path: {studio_exe}")
    else:
        print(f"\n❌ FAILED: Unable to launch Android Studio automatically")
        print(f"\n💡 Possible issues:")
        print("   1. Android Studio requires administrator privileges")
        print("   2. Android Studio is already running")
        print("   3. Windows security settings blocking the launch")
        print("   4. Corrupted Android Studio installation")
    
    print(f"\n🔧 Manual test:")
    print(f'   Try running: "{studio_exe}" "{test_project_path}"')

if __name__ == "__main__":
    main()