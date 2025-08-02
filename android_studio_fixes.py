#!/usr/bin/env python3
"""
Enhanced Android Studio project creation with fixes for common Gradle build errors
"""

import os
import logging
import shutil
from datetime import datetime

def create_enhanced_gradle_files(android_studio_path, app_path, project, package_name):
    """Create enhanced Gradle files with better error handling"""
    
    # Ensure project name is valid
    project_name = project.get('name', '').strip()
    if not project_name:
        project_name = 'APKEditorProject'
    
    # Sanitize project name for Gradle
    import re
    project_name = re.sub(r'[^a-zA-Z0-9_-]', '_', project_name)
    if not project_name or project_name[0].isdigit():
        project_name = 'APKEditorProject_' + project_name
    
    # Root build.gradle with enhanced configuration
    root_gradle_content = '''// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id 'com.android.application' version '8.1.0' apply false
    id 'com.android.library' version '8.1.0' apply false
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
'''
    
    with open(os.path.join(android_studio_path, 'build.gradle'), 'w') as f:
        f.write(root_gradle_content)
    
    # Enhanced app build.gradle with better error handling
    app_gradle_content = f'''plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
        
        // Prevent resource conflicts
        resourceConfigurations += ["en", "xxhdpi"]
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            debuggable false
        }}
        debug {{
            debuggable true
            minifyEnabled false
            applicationIdSuffix ".debug"
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
    
    buildFeatures {{
        viewBinding false
        dataBinding false
        aidl false
        renderScript false
        resValues false
        shaders false
    }}
    
    packagingOptions {{
        resources {{
            excludes += [
                'META-INF/DEPENDENCIES',
                'META-INF/LICENSE',
                'META-INF/LICENSE.txt',
                'META-INF/license.txt',
                'META-INF/NOTICE',
                'META-INF/NOTICE.txt',
                'META-INF/notice.txt',
                'META-INF/ASL2.0',
                'META-INF/*.kotlin_module',
                'META-INF/AL2.0',
                'META-INF/LGPL2.1'
            ]
        }}
    }}
    
    lintOptions {{
        checkReleaseBuilds false
        abortOnError false
        disable 'InvalidPackage', 'MissingTranslation', 'ExtraTranslation'
    }}
    
    // Prevent resource merging issues
    aaptOptions {{
        noCompress 'apk'
        ignoreAssetsPattern "!.svn:!.git:.*:!CVS:!thumbs.db:!picasa.ini:!*.scc:*~"
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.core:core:1.10.1'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'com.google.android.material:material:1.9.0'
    
    // Test dependencies
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}

// Prevent build cache issues
tasks.withType(JavaCompile) {{
    options.compilerArgs << "-Xlint:unchecked" << "-Xlint:deprecation"
}}
'''
    
    with open(os.path.join(app_path, 'build.gradle'), 'w') as f:
        f.write(app_gradle_content)
    
    # Enhanced settings.gradle
    settings_gradle_content = f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
        jcenter() // Warning: this repository is going to shut down soon
    }}
}}

rootProject.name = "{project_name}"
include ':app'
'''
    
    with open(os.path.join(android_studio_path, 'settings.gradle'), 'w') as f:
        f.write(settings_gradle_content)

def create_enhanced_proguard_rules(app_path):
    """Create comprehensive proguard rules to prevent build errors"""
    proguard_content = '''# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Disable optimization and obfuscation for debugging
-dontoptimize
-dontobfuscate
-ignorewarnings

# Keep all classes and methods to prevent runtime issues
-keep class ** { *; }
-keepattributes *

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep enums
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Keep Parcelable implementations
-keep class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}

# Keep Serializable classes
-keepnames class * implements java.io.Serializable
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

# Keep R class and its inner classes
-keep class **.R
-keep class **.R$* {
    <fields>;
}

# Keep custom views
-keep public class * extends android.view.View {
    public <init>(android.content.Context);
    public <init>(android.content.Context, android.util.AttributeSet);
    public <init>(android.content.Context, android.util.AttributeSet, int);
}

# Keep activities, services, receivers
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver
-keep public class * extends android.content.ContentProvider

# Suppress all warnings
-dontwarn **
'''
    
    proguard_path = os.path.join(app_path, 'proguard-rules.pro')
    with open(proguard_path, 'w', encoding='utf-8') as f:
        f.write(proguard_content)
    
    logging.info("Enhanced proguard-rules.pro created")

def create_gradle_wrapper_files(android_studio_path):
    """Create Gradle wrapper files for consistent builds"""
    
    # Create gradle wrapper directory
    gradle_wrapper_path = os.path.join(android_studio_path, 'gradle', 'wrapper')
    os.makedirs(gradle_wrapper_path, exist_ok=True)
    
    # gradle-wrapper.properties
    wrapper_properties_content = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
'''
    
    with open(os.path.join(gradle_wrapper_path, 'gradle-wrapper.properties'), 'w') as f:
        f.write(wrapper_properties_content)
    
    # gradlew (Unix)
    gradlew_content = '''#!/usr/bin/env sh

##############################################################################
##
##  Gradle start up script for UN*X
##
##############################################################################

# Attempt to set APP_HOME
# Resolve links: $0 may be a link
PRG="$0"
# Need this for relative symlinks.
while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \\(.*\\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \\"$PRG\\"`/" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

APP_NAME="Gradle"
APP_BASE_NAME=`basename "$0"`

# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD="maximum"

warn () {
    echo "$*"
}

die () {
    echo
    echo "$*"
    echo
    exit 1
}

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "`uname`" in
  CYGWIN* )
    cygwin=true
    ;;
  Darwin* )
    darwin=true
    ;;
  MINGW* )
    msys=true
    ;;
  NONSTOP* )
    nonstop=true
    ;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

# Determine the Java command to use to start the JVM.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        # IBM's JDK on AIX uses strange locations for the executables
        JAVACMD="$JAVA_HOME/jre/sh/java"
    else
        JAVACMD="$JAVA_HOME/bin/java"
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
    fi
else
    JAVACMD="java"
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
fi

# Increase the maximum file descriptors if we can.
if [ "$cygwin" = "false" -a "$darwin" = "false" -a "$nonstop" = "false" ] ; then
    MAX_FD_LIMIT=`ulimit -H -n`
    if [ $? -eq 0 ] ; then
        if [ "$MAX_FD" = "maximum" -o "$MAX_FD" = "max" ] ; then
            MAX_FD="$MAX_FD_LIMIT"
        fi
        ulimit -n $MAX_FD
        if [ $? -ne 0 ] ; then
            warn "Could not set maximum file descriptor limit: $MAX_FD"
        fi
    else
        warn "Could not query maximum file descriptor limit: $MAX_FD_LIMIT"
    fi
fi

# For Darwin, add options to specify how the application appears in the dock
if [ "$darwin" = "true" ]; then
    GRADLE_OPTS="$GRADLE_OPTS \\"-Xdock:name=$APP_NAME\\" \\"-Xdock:icon=$APP_HOME/media/gradle.icns\\""
fi

# For Cygwin or MSYS, switch paths to Windows format before running java
if [ "$cygwin" = "true" -o "$msys" = "true" ] ; then
    APP_HOME=`cygpath --path --mixed "$APP_HOME"`
    CLASSPATH=`cygpath --path --mixed "$CLASSPATH"`
    JAVACMD=`cygpath --unix "$JAVACMD"`

    # We build the pattern for arguments to be converted via cygpath
    ROOTDIRSRAW=`find -L / -maxdepth 1 -mindepth 1 -type d 2>/dev/null`
    SEP=""
    for dir in $ROOTDIRSRAW ; do
        ROOTDIRS="$ROOTDIRS$SEP$dir"
        SEP="|"
    done
    OURCYGPATTERN="(^($ROOTDIRS))"
    # Add a user-defined pattern to the cygpath arguments
    if [ "$GRADLE_CYGPATTERN" != "" ] ; then
        OURCYGPATTERN="$OURCYGPATTERN|($GRADLE_CYGPATTERN)"
    fi
    # Now convert the arguments - kludge to limit ourselves to /bin/sh
    i=0
    for arg in "$@" ; do
        CHECK=`echo "$arg"|egrep -c "$OURCYGPATTERN" -`
        CHECK2=`echo "$arg"|egrep -c "^-"`                                 ### Determine if an option

        if [ $CHECK -ne 0 ] && [ $CHECK2 -eq 0 ] ; then                    ### Added a condition
            eval `echo args$i`=`cygpath --path --ignore --mixed "$arg"`
        else
            eval `echo args$i`="\\"$arg\\""
        fi
        i=$((i+1))
    done
    case $i in
        (0) set -- ;;
        (1) set -- "$args0" ;;
        (2) set -- "$args0" "$args1" ;;
        (3) set -- "$args0" "$args1" "$args2" ;;
        (4) set -- "$args0" "$args1" "$args2" "$args3" ;;
        (5) set -- "$args0" "$args1" "$args2" "$args3" "$args4" ;;
        (6) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" ;;
        (7) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" ;;
        (8) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" "$args7" ;;
        (9) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" "$args7" "$args8" ;;
    esac
fi

# Escape application args
save () {
    for i do printf %s\\\\n "$i" | sed "s/'/'\\\\\\\\''/g;1s/^/'/;\$s/\$/' \\\\\\\\/" ; done
    echo " "
}
APP_ARGS=$(save "$@")

# Collect all arguments for the java command
set -- $DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS \\"-Dorg.gradle.appname=$APP_BASE_NAME\\" -classpath \\"$CLASSPATH\\" org.gradle.wrapper.GradleWrapperMain "$APP_ARGS"

# by using the same arguments order for every OS.
exec "$JAVACMD" "$@"
'''
    
    gradlew_path = os.path.join(android_studio_path, 'gradlew')
    with open(gradlew_path, 'w', newline='\n') as f:
        f.write(gradlew_content)
    
    # Make gradlew executable (Unix systems)
    try:
        os.chmod(gradlew_path, 0o755)
    except:
        pass  # Windows doesn't need this

def create_enhanced_project_files(android_studio_path, project):
    """Create enhanced project files with better configuration"""
    
    # Enhanced gradle.properties
    gradle_properties_content = '''# Project-wide Gradle settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true

# Gradle build optimization
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configureondemand=true

# Disable unnecessary features to speed up builds
android.enableBuildCache=true
android.enableR8.fullMode=false

# Suppress warnings
android.suppressUnsupportedCompileSdk=34
'''
    
    with open(os.path.join(android_studio_path, 'gradle.properties'), 'w') as f:
        f.write(gradle_properties_content)
    
    # Enhanced local.properties (optional)
    local_properties_content = '''# This file is automatically generated by Android Studio.
# Do not modify this file -- YOUR CHANGES WILL BE ERASED!
#
# This file should *NOT* be checked into Version Control Systems,
# as it contains information specific to your local configuration.
#
# Location of the SDK. This is only used by Gradle.
# For customization when using a Version Control System, please read the
# header note.
# sdk.dir=C:\\\\Users\\\\YourUsername\\\\AppData\\\\Local\\\\Android\\\\Sdk
'''
    
    with open(os.path.join(android_studio_path, 'local.properties'), 'w') as f:
        f.write(local_properties_content)
    
    # Create README for the Android Studio project
    readme_content = f'''# {project['name']} - Android Studio Project

This Android Studio project was automatically generated from a decompiled APK with enhanced build configuration.

## Build Fixes Applied

- ✅ Enhanced Gradle configuration for better compatibility
- ✅ Comprehensive ProGuard rules to prevent obfuscation issues
- ✅ Resource conflict resolution
- ✅ Build optimization settings
- ✅ Lint error suppression for decompiled code

## Project Structure

- `app/src/main/java/` - Java source code (converted from Smali)
- `app/src/main/res/` - Resources (layouts, images, strings, etc.)
- `app/src/main/assets/` - App assets
- `app/src/main/AndroidManifest.xml` - App manifest
- `app/proguard-rules.pro` - ProGuard configuration

## Build Instructions

1. **Open in Android Studio**: File → Open → Select this project folder
2. **Wait for Gradle Sync**: Let Android Studio download dependencies
3. **Build the Project**: Build → Make Project (Ctrl+F9)
4. **Run on Device**: Run → Run 'app' (Shift+F10)

## Troubleshooting

If you encounter build errors:

1. **Clean and Rebuild**: Build → Clean Project, then Build → Rebuild Project
2. **Invalidate Caches**: File → Invalidate Caches and Restart
3. **Check SDK**: Ensure Android SDK is properly configured
4. **Update Dependencies**: Check for newer versions in build.gradle

## Important Notes

1. **Smali to Java Conversion**: Original Smali code has been simplified for Android Studio compatibility
2. **Resource Cleanup**: Problematic resources have been cleaned or removed
3. **Build Optimization**: Project configured for faster builds and fewer errors
4. **ProGuard Disabled**: Obfuscation is disabled to prevent runtime issues

## Original APK Info

- **Original APK**: {project.get('original_apk', 'Unknown')}
- **Project Name**: {project['name']}
- **Conversion Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Build Configuration**: Enhanced for Gradle 8.5 compatibility

## Support

If you encounter issues:
1. Check the Android Studio Event Log for detailed error messages
2. Ensure you have the latest Android Studio and SDK tools
3. Verify Java JDK 8+ is installed and configured

Happy coding! 🚀
'''
    
    with open(os.path.join(android_studio_path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == '__main__':
    print("Android Studio Enhanced Project Creation")
    print("This module provides fixes for common Gradle build errors")