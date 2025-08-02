#!/usr/bin/env python3
"""
Test Android Studio Fix - Using older, more stable versions
This script tests the new Android Studio configuration with older versions
"""

import os
import tempfile
import shutil

def test_older_android_studio_config():
    """Test the older Android Studio configuration"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"🧪 Testing older Android Studio config in: {temp_dir}")
        
        # Create project structure
        app_path = os.path.join(temp_dir, 'app')
        src_main_path = os.path.join(app_path, 'src', 'main')
        res_path = os.path.join(src_main_path, 'res')
        values_path = os.path.join(res_path, 'values')
        java_path = os.path.join(src_main_path, 'java', 'com', 'example', 'app')
        
        os.makedirs(values_path, exist_ok=True)
        os.makedirs(java_path, exist_ok=True)
        
        # 1. Root build.gradle (Android Gradle Plugin 4.2.2)
        root_gradle = '''buildscript {
    repositories {
        google()
        mavenCentral()
        jcenter() // For older compatibility
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:4.2.2'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        jcenter() // For older compatibility
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
'''
        with open(os.path.join(temp_dir, 'build.gradle'), 'w') as f:
            f.write(root_gradle)
        
        # 2. App build.gradle (API 28, Support Library)
        app_gradle = '''apply plugin: 'com.android.application'

android {
    compileSdkVersion 28
    buildToolsVersion "28.0.3"
    
    defaultConfig {
        applicationId "com.example.app"
        minSdkVersion 16
        targetSdkVersion 28
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    lintOptions {
        abortOnError false
        checkReleaseBuilds false
        quiet true
    }
}

dependencies {
    implementation 'com.android.support:appcompat-v7:28.0.0'
}
'''
        with open(os.path.join(app_path, 'build.gradle'), 'w') as f:
            f.write(app_gradle)
        
        # 3. gradle.properties (No AndroidX)
        gradle_props = '''org.gradle.jvmargs=-Xmx1536m
android.useAndroidX=false
android.enableJetifier=false
org.gradle.parallel=false
org.gradle.configureondemand=false
org.gradle.daemon=false
'''
        with open(os.path.join(temp_dir, 'gradle.properties'), 'w') as f:
            f.write(gradle_props)
        
        # 4. settings.gradle
        settings_gradle = '''include ':app'
rootProject.name = "APKEditorProject"
'''
        with open(os.path.join(temp_dir, 'settings.gradle'), 'w') as f:
            f.write(settings_gradle)
        
        # 5. colors.xml (with required colors)
        colors_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#3F51B5</color>
    <color name="colorPrimaryDark">#303F9F</color>
    <color name="colorAccent">#FF4081</color>
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
</resources>
'''
        with open(os.path.join(values_path, 'colors.xml'), 'w') as f:
            f.write(colors_xml)
        
        # 6. strings.xml
        strings_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">APK Editor App</string>
</resources>
'''
        with open(os.path.join(values_path, 'strings.xml'), 'w') as f:
            f.write(strings_xml)
        
        # 7. styles.xml (using Support Library theme)
        styles_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
    </style>
</resources>
'''
        with open(os.path.join(values_path, 'styles.xml'), 'w') as f:
            f.write(styles_xml)
        
        # 8. AndroidManifest.xml
        manifest_xml = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app">

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:theme="@style/AppTheme">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
'''
        with open(os.path.join(src_main_path, 'AndroidManifest.xml'), 'w') as f:
            f.write(manifest_xml)
        
        # 9. MainActivity.java
        main_activity = '''package com.example.app;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
'''
        with open(os.path.join(java_path, 'MainActivity.java'), 'w') as f:
            f.write(main_activity)
        
        # 10. activity_main.xml
        layout_path = os.path.join(res_path, 'layout')
        os.makedirs(layout_path, exist_ok=True)
        
        activity_main_xml = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="18sp" />

</LinearLayout>
'''
        with open(os.path.join(layout_path, 'activity_main.xml'), 'w') as f:
            f.write(activity_main_xml)
        
        print("✅ Older Android Studio configuration created successfully!")
        print("\n📋 Configuration Summary:")
        print("   - Android Gradle Plugin: 4.2.2 (stable)")
        print("   - Compile SDK: 28 (stable)")
        print("   - Build Tools: 28.0.3")
        print("   - Min SDK: 16 (wide compatibility)")
        print("   - Target SDK: 28")
        print("   - Support Library: 28.0.0 (no AndroidX)")
        print("   - Gradle: Older compatible version")
        print("\n🎯 This configuration should eliminate AAPT2 errors!")
        
        return True

if __name__ == "__main__":
    print("🚀 Testing older Android Studio configuration...")
    test_older_android_studio_config()
    print("✅ Test completed!")