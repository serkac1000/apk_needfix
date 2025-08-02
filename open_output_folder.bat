@echo off
title APK Editor - Open Output Folder
echo ============================================================
echo APK Editor - Output Folder Access
echo ============================================================
echo.
echo Available project output folders:
echo.

REM List all project folders
for /d %%i in (projects\*) do (
    if exist "%%i\decompiled" (
        echo Project: %%~ni
        echo Location: %%i\decompiled\
        echo.
    )
)

echo ============================================================
echo Opening projects folder in File Explorer...
echo You can navigate to any project's 'decompiled' subfolder
echo to see the APK contents.
echo ============================================================

REM Open the projects folder in Windows Explorer
start explorer "projects"

pause