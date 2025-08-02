#!/usr/bin/env python3
"""
Direct fix for colors.xml to resolve AAPT color resource errors
This function creates the exact colors.xml file needed to fix the AAPT errors
"""

import os
import logging

def create_correct_colors_xml_final(res_path):
    """DIRECT FIX: Create colors.xml with exact color names AAPT is looking for"""
    try:
        values_path = os.path.join(res_path, 'values')
        os.makedirs(values_path, exist_ok=True)
        
        colors_xml_path = os.path.join(values_path, 'colors.xml')
        
        # EXACT colors.xml content that AAPT expects
        colors_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- EXACT color names that AAPT is looking for -->
    <color name="colorPrimary">#3F51B5</color>
    <color name="colorPrimaryDark">#303F9F</color>
    <color name="colorAccent">#FF4081</color>
    
    <!-- Basic colors for compatibility -->
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
    <color name="red">#FF0000</color>
    <color name="green">#00FF00</color>
    <color name="blue">#0000FF</color>
    <color name="gray">#808080</color>
    <color name="transparent">#00000000</color>
</resources>
'''
        
        # Force write the file
        with open(colors_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(colors_content)
        
        # Verify the file was created correctly
        if os.path.exists(colors_xml_path):
            with open(colors_xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'colorPrimary' in content and 'colorPrimaryDark' in content and 'colorAccent' in content:
                    print(f"✅ SUCCESS: colors.xml created with correct color names")
                    print(f"📁 File location: {colors_xml_path}")
                    return True
                else:
                    print(f"❌ ERROR: colors.xml created but missing required colors")
                    return False
        else:
            print(f"❌ ERROR: colors.xml file was not created")
            return False
        
    except Exception as e:
        print(f"❌ ERROR creating colors.xml: {e}")
        return False

if __name__ == "__main__":
    # Test the function
    test_res_path = "test_resources"
    create_correct_colors_xml_final(test_res_path)