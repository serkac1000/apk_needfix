#!/usr/bin/env python3
"""
FINAL COLOR FIX - Ultimate solution for AAPT color resource errors
This script creates a bulletproof colors.xml file that will resolve all color resource issues
"""

import os
import logging

def create_ultimate_color_fix(res_path):
    """Create the ultimate colors.xml file that fixes all AAPT color errors"""
    try:
        values_path = os.path.join(res_path, 'values')
        os.makedirs(values_path, exist_ok=True)
        
        # Create the most comprehensive colors.xml possible
        colors_xml_path = os.path.join(values_path, 'colors.xml')
        
        colors_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Required theme colors that AAPT is looking for -->
    <color name="colorPrimary">#3F51B5</color>
    <color name="colorPrimaryDark">#303F9F</color>
    <color name="colorAccent">#FF4081</color>
    
    <!-- Material Design colors -->
    <color name="material_blue_500">#2196F3</color>
    <color name="material_blue_700">#1976D2</color>
    <color name="material_pink_A200">#FF4081</color>
    
    <!-- Basic colors -->
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
    <color name="red">#FF0000</color>
    <color name="green">#00FF00</color>
    <color name="blue">#0000FF</color>
    <color name="gray">#808080</color>
    <color name="transparent">#00000000</color>
    
    <!-- Additional common colors -->
    <color name="light_gray">#CCCCCC</color>
    <color name="dark_gray">#666666</color>
    <color name="yellow">#FFFF00</color>
    <color name="orange">#FFA500</color>
    <color name="purple">#800080</color>
    
    <!-- AppCompat colors -->
    <color name="abc_primary_text_material_light">#DE000000</color>
    <color name="abc_secondary_text_material_light">#8A000000</color>
    <color name="abc_primary_text_material_dark">#FFFFFFFF</color>
    <color name="abc_secondary_text_material_dark">#B3FFFFFF</color>
</resources>
'''
        
        # Write with explicit UTF-8 encoding
        with open(colors_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(colors_content)
        
        # Create styles.xml with proper theme
        styles_xml_path = os.path.join(values_path, 'styles.xml')
        styles_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:Theme.Light">
        <!-- No custom attributes to avoid conflicts -->
    </style>
    
    <style name="AppTheme.NoActionBar">
        <item name="android:windowActionBar">false</item>
        <item name="android:windowNoTitle">true</item>
    </style>
</resources>
'''
        
        with open(styles_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(styles_content)
        
        # Create strings.xml
        strings_xml_path = os.path.join(values_path, 'strings.xml')
        strings_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">APK Editor App</string>
    <string name="hello_world">Hello World!</string>
    <string name="action_settings">Settings</string>
</resources>
'''
        
        with open(strings_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(strings_content)
        
        print(f"✅ Ultimate color fix applied successfully!")
        print(f"📁 Created files in: {values_path}")
        print(f"   - colors.xml (with all required colors)")
        print(f"   - styles.xml (minimal theme)")
        print(f"   - strings.xml (basic strings)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating ultimate color fix: {e}")
        return False

if __name__ == "__main__":
    # Test the function
    test_res_path = "test_resources"
    create_ultimate_color_fix(test_res_path)