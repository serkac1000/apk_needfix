@echo off
echo Testing Android Studio Launch
echo =============================

echo.
echo Checking common Android Studio locations:

set "STUDIO_PATH="

if exist "C:\Program Files\Android\Android Studio\bin\studio64.exe" (
    echo ✅ Found: C:\Program Files\Android\Android Studio\bin\studio64.exe
    set "STUDIO_PATH=C:\Program Files\Android\Android Studio\bin\studio64.exe"
    goto :found
)

if exist "C:\Program Files (x86)\Android\Android Studio\bin\studio64.exe" (
    echo ✅ Found: C:\Program Files (x86)\Android\Android Studio\bin\studio64.exe
    set "STUDIO_PATH=C:\Program Files (x86)\Android\Android Studio\bin\studio64.exe"
    goto :found
)

if exist "%USERPROFILE%\AppData\Local\Android\Studio\bin\studio64.exe" (
    echo ✅ Found: %USERPROFILE%\AppData\Local\Android\Studio\bin\studio64.exe
    set "STUDIO_PATH=%USERPROFILE%\AppData\Local\Android\Studio\bin\studio64.exe"
    goto :found
)

echo ❌ Android Studio not found in common locations
echo.
echo Please check if Android Studio is installed and note the installation path.
pause
exit /b 1

:found
echo.
echo Found Android Studio at: %STUDIO_PATH%
echo.
echo Testing launch...
echo.

rem Try to launch Android Studio
start "" "%STUDIO_PATH%"

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: Android Studio launched successfully!
    echo.
    echo This path should work for auto-launch: %STUDIO_PATH%
) else (
    echo ❌ FAILED: Could not launch Android Studio
    echo Error level: %ERRORLEVEL%
)

echo.
pause