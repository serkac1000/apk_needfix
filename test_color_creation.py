#!/usr/bin/env python3
"""
Test script to verify colors.xml creation and identify the root cause
"""

import os
import tempfile
import shutil

def test_color_creation():
    """Test the color creation process to identify issues"""
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Testing in: {temp_dir}")
        
        # Create res/values structure
        values_path = os.path.join(temp_dir, 'res', 'values')
        os.makedirs(values_path, exist_ok=True)
        
        # Create colors.xml
        colors_xml_path = os.path.join(values_path, 'colors.xml')
        colors_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#3F51B5</color>
    <color name="colorPrimaryDark">#303F9F</color>
    <color name="colorAccent">#FF4081</color>
</resources>
'''
        
        print("Creating colors.xml...")
        with open(colors_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(colors_content)
        
        # Verify file exists
        if os.path.exists(colors_xml_path):
            print("✅ colors.xml file created successfully")
            
            # Check file size
            file_size = os.path.getsize(colors_xml_path)
            print(f"📏 File size: {file_size} bytes")
            
            # Read and verify content
            with open(colors_xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"📄 Content length: {len(content)} characters")
                
                if 'colorPrimary' in content:
                    print("✅ colorPrimary found in content")
                else:
                    print("❌ colorPrimary NOT found in content")
                
                if 'colorPrimaryDark' in content:
                    print("✅ colorPrimaryDark found in content")
                else:
                    print("❌ colorPrimaryDark NOT found in content")
                
                if 'colorAccent' in content:
                    print("✅ colorAccent found in content")
                else:
                    print("❌ colorAccent NOT found in content")
                
                print("\n📝 Full content:")
                print(content)
                
        else:
            print("❌ colors.xml file was NOT created")
        
        # List all files in the directory
        print(f"\n📁 Files in {values_path}:")
        if os.path.exists(values_path):
            for file in os.listdir(values_path):
                file_path = os.path.join(values_path, file)
                size = os.path.getsize(file_path)
                print(f"   {file} ({size} bytes)")
        else:
            print("   Directory does not exist")

if __name__ == "__main__":
    test_color_creation()