def create_proguard_rules(app_path):
    """Create proguard-rules.pro file to prevent build errors"""
    try:
        proguard_content = '''# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile

# Keep all classes and methods to prevent obfuscation issues
-keep class ** { *; }
-keepattributes *

# Prevent optimization issues
-dontoptimize
-dontobfuscate

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
'''
        
        proguard_path = os.path.join(app_path, 'proguard-rules.pro')
        with open(proguard_path, 'w', encoding='utf-8') as f:
            f.write(proguard_content)
        
        print(f"Created proguard-rules.pro at {proguard_path}")
        
    except Exception as e:
        print(f"Error creating proguard rules: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        create_proguard_rules(sys.argv[1])
    else:
        print("Usage: python proguard_fix.py <app_path>")