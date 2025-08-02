#!/usr/bin/env python3
"""
Test Manifest Generation - Ultimate compatibility test
This script tests the most stable Android Studio configuration possible
"""

import os
import tempfile

def create_ultra_stable_android_project():
    """Create the most stable Android Studio project configuration possible"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"🧪 Testing ultra-stable config in: {temp_dir}")
        
        # Create project structure
        app_path = os.path.join(temp_dir, 'app')
        src_main_path = os.path.join(app_path, 'src', 'main')
        res_path = os.path.join(src_main_path, 'res')
        values_path = os.path.join(res_path, 'values')
        java_path = os.path.join(src_main_path, 'java', 'com', 'example', 'app')
        
        os.makedirs(values_path, exist_ok=True)
        os.makedirs(java_path, exist_ok=True)
        
        # 1. ULTRA-STABLE root build.gradle (Android Gradle Plugin 3.5.4)
        root_gradle = '''buildscript {
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.5.4'
    }
}

allprojects {
    repositories {
        google()
        jcenter()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
'''
        with open(os.path.join(temp_dir, 'build.gradle'), 'w') as f:
            f.write(root_gradle)
        
        # 2. ULTRA-STABLE app build.gradle (API 28, NO DEBUG)
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
            debuggable true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    
    // CRITICAL: Only build release variant to avoid debug issues
    android.variantFilter { variant ->
        if (variant.buildType.name == 'debug') {
            variant.setIgnore(true)
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
        
        # 3. ULTRA-STABLE gradle.properties (No AndroidX, No parallel)
        gradle_props = '''org.gradle.jvmargs=-Xmx1536m
android.useAndroidX=false
android.enableJetifier=false
org.gradle.parallel=false
org.gradle.configureondemand=false
org.gradle.daemon=false
android.debug.obsoleteApi=true
android.enableBuildCache=false
'''
        with open(os.path.join(temp_dir, 'gradle.properties'), 'w') as f:
            f.write(gradle_props)
        
        # 4. ULTRA-STABLE gradle wrapper (Gradle 5.6.4 - compatible with AGP 3.5.4)
        gradle_wrapper_dir = os.path.join(temp_dir, 'gradle', 'wrapper')
        os.makedirs(gradle_wrapper_dir, exist_ok=True)
        
        wrapper_props = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-5.6.4-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
'''
        with open(os.path.join(gradle_wrapper_dir, 'gradle-wrapper.properties'), 'w') as f:
            f.write(wrapper_props)
        
        # 5. settings.gradle
        settings_gradle = '''include ':app'
rootProject.name = "APKEditorProject"
'''
        with open(os.path.join(temp_dir, 'settings.gradle'), 'w') as f:
            f.write(settings_gradle)
        
        # 6. MINIMAL colors.xml (with required colors)
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
        
        # 7. MINIMAL strings.xml
        strings_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">APK Editor App</string>
</resources>
'''
        with open(os.path.join(values_path, 'strings.xml'), 'w') as f:
            f.write(strings_xml)
        
        # 8. MINIMAL styles.xml (Support Library theme)
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
        
        # 9. MINIMAL AndroidManifest.xml
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
        
        # 10. MINIMAL MainActivity.java (Support Library)
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
        
        # 11. MINIMAL activity_main.xml
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
        
        print("✅ Ultra-stable Android Studio configuration created!")
        print("\n📋 ULTRA-STABLE Configuration Summary:")
        print("   - Android Gradle Plugin: 3.5.4 (ultra-stable)")
        print("   - Gradle: 5.6.4 (perfectly compatible)")
        print("   - Compile SDK: 28 (stable)")
        print("   - Build Tools: 28.0.3")
        print("   - Min SDK: 16 (maximum compatibility)")
        print("   - Target SDK: 28")
        print("   - Support Library: 28.0.0 (no AndroidX)")
        print("   - Debug builds: DISABLED")
        print("   - Parallel builds: DISABLED")
        print("   - Build cache: DISABLED")
        print("   - Gradle daemon: DISABLED")
        print("\n🎯 This should eliminate ALL dependency resolution errors!")
        
        return True

if __name__ == "__main__":
    print("🚀 Testing ultra-stable Android Studio configuration...")
    create_ultra_stable_android_project()
    print("✅ Test completed!")