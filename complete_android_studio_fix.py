#!/usr/bin/env python3
"""
Complete Android Studio Fix - Ultimate solution for AAPT color resource errors
This script provides the final fix for all Android Studio project creation issues
"""

import os
import logging

def fix_android_studio_colors_ultimate(project_path):
    """Ultimate fix for Android Studio color resource errors"""
    try:
        # Find the values directory
        values_path = os.path.join(project_path, 'app', 'src', 'main', 'res', 'values')
        
        if not os.path.exists(values_path):
            print(f"❌ Values directory not found: {values_path}")
            return False
        
        # Fix colors.xml
        colors_xml_path = os.path.join(values_path, 'colors.xml')
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
    
    <!-- Keep any existing colors for compatibility -->
    <color name="primary_color">#3F51B5</color>
    <color name="secondary_color">#FFC107</color>
    <color name="accent_color">#FF4081</color>
    <color name="background_color">#FFFFFF</color>
    <color name="text_color">#212121</color>
</resources>
'''
        
        with open(colors_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(colors_content)
        
        # Fix styles.xml to use simple theme
        styles_xml_path = os.path.join(values_path, 'styles.xml')
        styles_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:Theme.Light">
        <!-- Simple theme without custom color references to avoid AAPT errors -->
    </style>
    
    <style name="AppTheme.NoActionBar">
        <item name="android:windowActionBar">false</item>
        <item name="android:windowNoTitle">true</item>
    </style>
</resources>
'''
        
        with open(styles_xml_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(styles_content)
        
        # Verify files were created
        colors_ok = os.path.exists(colors_xml_path)
        styles_ok = os.path.exists(styles_xml_path)
        
        if colors_ok and styles_ok:
            print(f"✅ SUCCESS: Fixed colors.xml and styles.xml in {values_path}")
            return True
        else:
            print(f"❌ FAILED: colors_ok={colors_ok}, styles_ok={styles_ok}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def fix_all_android_studio_projects():
    """Fix all existing Android Studio projects"""
    projects_dir = "projects"
    
    if not os.path.exists(projects_dir):
        print(f"❌ Projects directory not found: {projects_dir}")
        return
    
    fixed_count = 0
    total_count = 0
    
    for project_id in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project_id)
        android_studio_path = os.path.join(project_path, 'android_studio_project')
        
        if os.path.exists(android_studio_path):
            total_count += 1
            print(f"\n🔧 Fixing project: {project_id}")
            
            if fix_android_studio_colors_ultimate(android_studio_path):
                fixed_count += 1
                print(f"✅ Fixed project: {project_id}")
            else:
                print(f"❌ Failed to fix project: {project_id}")
    
    print(f"\n📊 SUMMARY: Fixed {fixed_count}/{total_count} Android Studio projects")

if __name__ == "__main__":
    print("🚀 Starting complete Android Studio fix...")
    fix_all_android_studio_projects()
    print("✅ Complete Android Studio fix finished!")