import os
import shutil
import json
import logging
import zipfile
from datetime import datetime
from utils.apktool import APKTool
from utils.file_manager import FileManager
from werkzeug.utils import secure_filename

class APKEditor:
    def __init__(self, projects_folder, temp_folder):
        self.projects_folder = projects_folder
        self.temp_folder = temp_folder
        self.apktool = APKTool()
        self.file_manager = FileManager(projects_folder)

    def decompile_apk(self, apk_path, project_id, project_name):
        """Decompile APK and create project"""
        try:
            # Create project directory
            project_dir = os.path.join(self.projects_folder, project_id)
            os.makedirs(project_dir, exist_ok=True)

            # Decompile APK
            decompiled_dir = os.path.join(project_dir, 'decompiled')
            success = self.apktool.decompile(apk_path, decompiled_dir)

            if success:
                # Create project metadata
                metadata = {
                    'id': project_id,
                    'name': project_name,
                    'original_apk': os.path.basename(apk_path),
                    'created_at': datetime.now().isoformat(),
                    'status': 'decompiled',
                    'resources_available': True
                }

                # Save metadata
                metadata_path = os.path.join(project_dir, 'metadata.json')
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)

                # Copy original APK to project
                shutil.copy2(apk_path, os.path.join(project_dir, 'original.apk'))

                # Ensure essential Android structure exists
                self._ensure_android_structure(decompiled_dir)

                logging.info(f"APK decompiled successfully: {project_id}")
                return True
            else:
                # Clean up on failure
                if os.path.exists(project_dir):
                    shutil.rmtree(project_dir)
                return False

        except Exception as e:
            logging.error(f"Decompile error: {str(e)}")
            return False

    def _ensure_android_structure(self, decompiled_dir):
        """Ensure proper Android project structure"""
        try:
            # Create essential directories
            essential_dirs = [
                'res/layout',
                'res/values',
                'res/drawable-hdpi',
                'res/drawable-mdpi',
                'res/drawable-xhdpi',
                'res/drawable-xxhdpi',
                'smali/com/example/app',
                'assets'
            ]

            for dir_path in essential_dirs:
                full_path = os.path.join(decompiled_dir, dir_path)
                os.makedirs(full_path, exist_ok=True)

            # Ensure AndroidManifest.xml exists
            manifest_path = os.path.join(decompiled_dir, 'AndroidManifest.xml')
            if not os.path.exists(manifest_path):
                self._create_default_manifest(manifest_path)

            # Ensure strings.xml exists
            strings_path = os.path.join(decompiled_dir, 'res/values/strings.xml')
            if not os.path.exists(strings_path):
                self._create_default_strings(strings_path)

            # Ensure colors.xml exists
            colors_path = os.path.join(decompiled_dir, 'res/values/colors.xml')
            if not os.path.exists(colors_path):
                self._create_default_colors(colors_path)

            # Ensure main layout exists
            layout_path = os.path.join(decompiled_dir, 'res/layout/activity_main.xml')
            if not os.path.exists(layout_path):
                self._create_default_layout(layout_path)

        except Exception as e:
            logging.warning(f"Error ensuring Android structure: {str(e)}")

    def _create_default_manifest(self, manifest_path):
        """Create default AndroidManifest.xml"""
        manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.modifiedapp"
    android:versionCode="1"
    android:versionName="1.0">

    <uses-sdk
        android:minSdkVersion="21"
        android:targetSdkVersion="33" />

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:theme="@style/AppTheme">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@android:style/Theme.Material">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''

        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest_content)

    def _create_default_strings(self, strings_path):
        """Create default strings.xml"""
        strings_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Modified App</string>
    <string name="hello_world">Hello World!</string>
    <string name="button_text">Click Me</string>
    <string name="button1_text">Button 1</string>
    <string name="button2_text">Button 2</string>
    <string name="button3_text">Button 3</string>
</resources>'''

        os.makedirs(os.path.dirname(strings_path), exist_ok=True)
        with open(strings_path, 'w', encoding='utf-8') as f:
            f.write(strings_content)

    def _create_default_colors(self, colors_path):
        """Create default colors.xml"""
        colors_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary_color">#2196F3</color>
    <color name="secondary_color">#FFC107</color>
    <color name="accent_color">#FF5722</color>
    <color name="background_color">#FFFFFF</color>
    <color name="text_color">#212121</color>
</resources>'''

        os.makedirs(os.path.dirname(colors_path), exist_ok=True)
        with open(colors_path, 'w', encoding='utf-8') as f:
            f.write(colors_content)

    def _create_default_layout(self, layout_path):
        """Create default activity_main.xml layout"""
        layout_content = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        android:textSize="18sp"
        android:layout_marginBottom="24dp" />

    <Button
        android:id="@+id/button1"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/button1_text"
        android:layout_marginBottom="16dp" />

    <Button
        android:id="@+id/button2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/button2_text"
        android:layout_marginBottom="16dp" />

    <Button
        android:id="@+id/button3"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/button3_text" />

</LinearLayout>'''

        os.makedirs(os.path.dirname(layout_path), exist_ok=True)
        with open(layout_path, 'w', encoding='utf-8') as f:
            f.write(layout_content)

    def get_project_resources(self, project_id):
        """Get available resources for editing"""
        project_dir = os.path.join(self.projects_folder, project_id)
        decompiled_dir = os.path.join(project_dir, 'decompiled')

        resources = {
            'images': [],
            'strings': [],
            'layouts': []
        }

        try:
            # Get drawable resources (images)
            drawable_dirs = [
                'res/drawable',
                'res/drawable-hdpi',
                'res/drawable-mdpi', 
                'res/drawable-xhdpi',
                'res/drawable-xxhdpi',
                'res/drawable-xxxhdpi'
            ]

            for drawable_dir in drawable_dirs:
                dir_path = os.path.join(decompiled_dir, drawable_dir)
                if os.path.exists(dir_path):
                    for filename in os.listdir(dir_path):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                            resources['images'].append({
                                'name': filename,
                                'path': os.path.join(drawable_dir, filename),
                                'folder': drawable_dir
                            })

            # Get string resources
            strings_path = os.path.join(decompiled_dir, 'res/values/strings.xml')
            if os.path.exists(strings_path):
                resources['strings'].append({
                    'name': 'strings.xml',
                    'path': 'res/values/strings.xml',
                    'type': 'strings'
                })

            # Get colors
            colors_path = os.path.join(decompiled_dir, 'res/values/colors.xml')
            if os.path.exists(colors_path):
                resources['strings'].append({
                    'name': 'colors.xml',
                    'path': 'res/values/colors.xml',
                    'type': 'colors'
                })

            # Get layout resources
            layout_dir = os.path.join(decompiled_dir, 'res/layout')
            if os.path.exists(layout_dir):
                for filename in os.listdir(layout_dir):
                    if filename.endswith('.xml'):
                        resources['layouts'].append({
                            'name': filename,
                            'path': os.path.join('res/layout', filename),
                            'type': 'layout'
                        })

            return resources

        except Exception as e:
            logging.error(f"Error getting resources: {str(e)}")
            return resources

    def get_resource_content(self, project_id, resource_type, resource_path):
        """Get content of a specific resource"""
        try:
            project_dir = os.path.join(self.projects_folder, project_id)
            decompiled_dir = os.path.join(project_dir, 'decompiled')
            file_path = os.path.join(decompiled_dir, resource_path)

            if os.path.exists(file_path):
                if resource_type in ['string', 'layout']:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    return {'exists': True, 'path': file_path}
            else:
                return ""

        except Exception as e:
            logging.error(f"Error getting resource content: {str(e)}")
            return ""

    def save_image_resource(self, project_id, resource_path, file):
        """Save image resource"""
        try:
            project_dir = os.path.join(self.projects_folder, project_id)
            decompiled_dir = os.path.join(project_dir, 'decompiled')
            file_path = os.path.join(decompiled_dir, resource_path)

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save file
            file.save(file_path)
            logging.info(f"Image resource saved: {resource_path}")
            return True

        except Exception as e:
            logging.error(f"Error saving image resource: {str(e)}")
            return False

    def save_string_resource(self, project_id, resource_path, content):
        """Save string resource"""
        try:
            project_dir = os.path.join(self.projects_folder, project_id)
            decompiled_dir = os.path.join(project_dir, 'decompiled')
            file_path = os.path.join(decompiled_dir, resource_path)

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logging.info(f"String resource saved: {resource_path}")
            return True

        except Exception as e:
            logging.error(f"Error saving string resource: {str(e)}")
            return False

    def save_layout_resource(self, project_id, resource_path, content):
        """Save layout resource"""
        try:
            project_dir = os.path.join(self.projects_folder, project_id)
            decompiled_dir = os.path.join(project_dir, 'decompiled')
            file_path = os.path.join(decompiled_dir, resource_path)

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logging.info(f"Layout resource saved: {resource_path}")
            return True

        except Exception as e:
            logging.error(f"Error saving layout resource: {str(e)}")
            return False


    def compile_apk(self, project_id):
        """Compile modified APK"""
        try:
            project_dir = os.path.join(self.projects_folder, project_id)
            decompiled_dir = os.path.join(project_dir, 'decompiled')
            output_path = os.path.join(project_dir, 'compiled.apk')

            # Compile APK
            success = self.apktool.compile(decompiled_dir, output_path)

            if success and os.path.exists(output_path):
                # Validate APK structure
                if self._validate_apk_structure(output_path):
                    # Sign APK
                    signed_path = os.path.join(project_dir, 'signed.apk')
                    sign_success = self.apktool.sign_apk(output_path, signed_path)

                    if sign_success and os.path.exists(signed_path):
                        # Final validation of signed APK
                        if self._validate_signed_apk(signed_path):
                            logging.info(f"APK compiled and signed successfully: {project_id}")
                            return signed_path
                        else:
                            logging.warning(f"Signed APK validation failed, returning unsigned: {project_id}")
                            return output_path
                    else:
                        logging.warning(f"APK compiled but signing failed: {project_id}")
                        return output_path
                else:
                    logging.error(f"APK structure validation failed: {project_id}")
                    return None
            else:
                logging.error(f"APK compilation failed: {project_id}")
                return None

        except Exception as e:
            logging.error(f"Compile error: {str(e)}")
            return None

    def _validate_apk_structure(self, apk_path):
        """Validate APK has required structure for Android"""
        try:
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                filenames = apk_zip.namelist()

                # Check for required files
                required_files = ['AndroidManifest.xml']
                for required_file in required_files:
                    if required_file not in filenames:
                        logging.error(f"Missing required file: {required_file}")
                        return False

                # Check for classes.dex or similar
                has_dex = any(f.endswith('.dex') for f in filenames)
                if not has_dex:
                    logging.warning("No DEX files found - APK may not be installable")

                logging.info("APK structure validation passed")
                return True

        except Exception as e:
            logging.error(f"APK validation error: {str(e)}")
            return False

    def _validate_signed_apk(self, apk_path):
        """Validate signed APK has proper signature files"""
        try:
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                filenames = apk_zip.namelist()

                # Check for signature files
                signature_files = ['META-INF/MANIFEST.MF', 'META-INF/CERT.SF', 'META-INF/CERT.RSA']
                missing_sig_files = [f for f in signature_files if f not in filenames]

                if missing_sig_files:
                    logging.warning(f"Missing signature files: {missing_sig_files}")
                    return False

                logging.info("Signed APK validation passed")
                return True

        except Exception as e:
            logging.error(f"Signed APK validation error: {str(e)}")
            return False

    def get_compiled_apk_path(self, project_id):
        """Get path to compiled APK"""
        project_dir = os.path.join(self.projects_folder, project_id)

        # Check for signed APK first
        signed_path = os.path.join(project_dir, 'signed.apk')
        if os.path.exists(signed_path):
            return signed_path

        # Fall back to compiled APK
        compiled_path = os.path.join(project_dir, 'compiled.apk')
        if os.path.exists(compiled_path):
            return compiled_path

        return None

    def sign_apk_advanced(self, compiled_apk_path, output_path):
        """Advanced APK signing with proper certificate chain"""
        try:
            return self.apktool.sign_apk(compiled_apk_path, output_path)
        except Exception as e:
            logging.error(f"Error signing APK: {str(e)}")
            return False

    def force_save_project(self, project_id):
        """Force save all project changes to ensure persistence"""
        try:
            project_dir = os.path.join(self.projects_folder, project_id)
            if os.path.exists(project_dir):
                # Force sync all files in project directory
                for root, dirs, files in os.walk(project_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r+b') as f:
                                f.flush()
                                os.fsync(f.fileno())
                        except Exception:
                            pass  # Skip files that can't be synced

                logging.info(f"Project {project_id} force saved successfully")
                return True
            return False
        except Exception as e:
            logging.error(f"Error force saving project {project_id}: {str(e)}")
            return False