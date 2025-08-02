# GUI Output Directory

This directory contains the output from GUI-based APK decompilation operations.

## Structure

- `decompiled/` - Contains decompiled APK files organized by project
- Each project gets its own subdirectory with the project ID as the folder name
- Decompiled contents include:
  - `AndroidManifest.xml` - App manifest file
  - `res/` - Resources (images, layouts, strings, etc.)
  - `smali/` - Decompiled Java code in Smali format
  - `assets/` - App assets
  - `original/` - Original APK backup
  - `apktool.yml` - APKTool configuration

## Usage

When you decompile an APK through the web interface, the extracted files will be placed in:
```
gui_output/decompiled/{project_id}/
```

This allows for easy browsing and editing of APK contents through the web interface.

## Notes

- This directory is automatically managed by the application
- Files here are temporary and tied to active projects
- Clean up old projects regularly to save disk space