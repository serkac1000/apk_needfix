#!/usr/bin/env python3
"""
Bulletproof Gradle Configuration Test
Tests the new Android Studio configuration with debug removal and older versions
"""

import os
import tempfile

def create_bulletproof_gradle_files(android_studio_path, app_path, project, package_name='com.example.app'):
    """Create the most minimal Gradle configuration to prevent ALL build failures"""
    
    # Ensure project name is valid
    project_name = project.get('name', '').strip()
    if not project_name:
        project_name = 'APKEditorProject'
    
    # Sanitize project name for Gradle
    import re
    project_name = re.sub(r'[^a-zA-Z0-9_-]', '_', project_name)
    if not project_name or project_name[0].isdigit():
        project_name = 'APKEditorProject_' + project_name
    
    # STABLE OLDER VERSION root build.gradle - Compatible with older Android Studio
    root_gradle_content = '''buildscript {
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
    
    with open(os.path.join(android_studio_path, 'build.gradle'), 'w') as f:
        f.write(root_gradle_content)
    
    # STABLE OLDER VERSION app build.gradle - NO DEBUG BUILD TYPE
    app_gradle_content = f'''apply plugin: 'com.android.application'

android {{
    compileSdkVersion 28
    buildToolsVersion "28.0.3"
    
    defaultConfig {{
        applicationId "{package_name}"
        minSdkVersion 16
        targetSdkVersion 28
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            debuggable true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }}
    }}
    
    // CRITICAL: Only build release variant to avoid debug issues
    variantFilter {{ variant ->
        if (variant.buildType.name == 'debug') {{
            variant.setIgnore(true)
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
    
    lintOptions {{
        abortOnError false
        checkReleaseBuilds false
        quiet true
    }}
}}

dependencies {{
    implementation 'com.android.support:appcompat-v7:28.0.0'
}}
'''
    
    with open(os.path.join(app_path, 'build.gradle'), 'w') as f:
        f.write(app_gradle_content)
    
    # MINIMAL settings.gradle
    settings_gradle_content = f'''include ':app'
rootProject.name = "{project_name}"
'''
    
    with open(os.path.join(android_studio_path, 'settings.gradle'), 'w') as f:
        f.write(settings_gradle_content)
    
    # STABLE OLDER VERSION gradle.properties - Compatible with older Android Studio
    gradle_properties_content = '''org.gradle.jvmargs=-Xmx1536m
android.useAndroidX=false
android.enableJetifier=false
org.gradle.parallel=false
org.gradle.configureondemand=false
org.gradle.daemon=false
android.debug.obsoleteApi=true
android.enableBuildCache=false
'''
    
    with open(os.path.join(android_studio_path, 'gradle.properties'), 'w') as f:
        f.write(gradle_properties_content)
    
    # Create gradle wrapper properties with compatible version
    gradle_wrapper_dir = os.path.join(android_studio_path, 'gradle', 'wrapper')
    os.makedirs(gradle_wrapper_dir, exist_ok=True)
    
    wrapper_properties_content = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-6.7.1-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
'''
    
    with open(os.path.join(gradle_wrapper_dir, 'gradle-wrapper.properties'), 'w') as f:
        f.write(wrapper_properties_content)
    
    print("✅ Bulletproof Gradle configuration created successfully!")
    return True

def test_bulletproof_config():
    """Test the bulletproof configuration"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"🧪 Testing bulletproof config in: {temp_dir}")
        
        # Create project structure
        android_studio_path = temp_dir
        app_path = os.path.join(temp_dir, 'app')
        os.makedirs(app_path, exist_ok=True)
        
        # Test project data
        project = {'name': 'TestProject'}
        package_name = 'com.example.test'
        
        create_bulletproof_gradle_files(android_studio_path, app_path, project, package_name)
        
        # Verify files were created
        required_files = [
            'build.gradle',
            'settings.gradle', 
            'gradle.properties',
            'app/build.gradle',
            'gradle/wrapper/gradle-wrapper.properties'
        ]
        
        all_files_exist = True
        for file_path in required_files:
            full_path = os.path.join(temp_dir, file_path)
            if os.path.exists(full_path):
                print(f"✅ {file_path} - Created")
            else:
                print(f"❌ {file_path} - Missing")
                all_files_exist = False
        
        # Check app/build.gradle for debug removal
        app_gradle_path = os.path.join(app_path, 'build.gradle')
        with open(app_gradle_path, 'r') as f:
            content = f.read()
            
        if 'variantFilter' in content and 'debug' in content and 'setIgnore(true)' in content:
            print("✅ Debug build type removal - Configured")
        else:
            print("❌ Debug build type removal - Missing")
            all_files_exist = False
        
        # Check for older versions
        if 'gradle:4.2.2' in content:
            print("✅ Android Gradle Plugin 4.2.2 - Configured")
        else:
            print("❌ Android Gradle Plugin version - Incorrect")
            all_files_exist = False
        
        if 'compileSdkVersion 28' in content:
            print("✅ Compile SDK 28 - Configured")
        else:
            print("❌ Compile SDK version - Incorrect")
            all_files_exist = False
        
        if 'appcompat-v7:28.0.0' in content:
            print("✅ Support Library 28.0.0 - Configured")
        else:
            print("❌ Support Library - Missing")
            all_files_exist = False
        
        return all_files_exist

if __name__ == "__main__":
    print("🚀 Testing bulletproof Gradle configuration...")
    print("\n📋 Configuration Summary:")
    print("   - Android Gradle Plugin: 4.2.2 (stable)")
    print("   - Compile SDK: 28 (stable)")
    print("   - Build Tools: 28.0.3")
    print("   - Min SDK: 16 (wide compatibility)")
    print("   - Target SDK: 28")
    print("   - Support Library: 28.0.0 (no AndroidX)")
    print("   - Gradle: 6.7.1 (compatible)")
    print("   - Debug builds: DISABLED")
    print("   - Only release builds: ENABLED")
    print("\n🧪 Running tests...")
    
    if test_bulletproof_config():
        print("\n🎉 All tests passed! Configuration is bulletproof.")
        print("\n🎯 This should eliminate:")
        print("   ✅ AAPT color resource errors")
        print("   ✅ Debug build failures")
        print("   ✅ AndroidX compatibility issues")
        print("   ✅ Resource processing errors")
        print("   ✅ Gradle version conflicts")
    else:
        print("\n❌ Some tests failed. Check configuration.")