@echo off
title APK Editor Pro - Auto Setup and Start
echo ========================================
echo APK Editor Pro - Automatic Setup
echo ========================================
echo.

REM Use hardcoded Python path
set "PYTHON_EXE=C:\Users\serka\AppData\Local\Programs\Python\Python312\python.exe"

REM Check if Python exists at hardcoded path
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at: %PYTHON_EXE%
    echo Please verify Python is installed at this location
    pause
    exit /b 1
) else (
    echo Python found at: %PYTHON_EXE%
)

REM Check if pip is available
"%PYTHON_EXE%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
) else (
    echo pip found: OK
)

echo [1/6] Installing Python dependencies...
"%PYTHON_EXE%" -m pip install flask werkzeug requests --quiet
if errorlevel 1 (
    echo WARNING: Some Python packages may have failed to install
) else (
    echo Python dependencies installed: OK
)

echo [2/6] Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "projects" mkdir projects
if not exist "temp" mkdir temp
if not exist "tools" mkdir tools

echo [3/6] Checking for Java...
java -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Java not found. Downloading OpenJDK...
    echo This may take a few minutes...
    
    REM Download portable OpenJDK
    if not exist "tools\jdk" (
        echo Downloading OpenJDK 11...
        powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13; Invoke-WebRequest -Uri 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.19+7/OpenJDK11U-jdk_x64_windows_hotspot_11.0.19_7.zip' -OutFile 'tools\openjdk.zip' -ErrorAction Stop}" || (
            echo ERROR: Failed to download OpenJDK
            pause
            exit /b 1
        )
        
        if exist "tools\openjdk.zip" (
            echo Extracting OpenJDK...
            powershell -Command "Expand-Archive -Path 'tools\openjdk.zip' -DestinationPath 'tools\' -Force"
            ren "tools\jdk-11.0.19+7" "jdk"
            del "tools\openjdk.zip"
            echo OpenJDK installed successfully
        )
    )
    
    REM Add Java to PATH for this session
    set "JAVA_HOME=%~dp0tools\jdk"
    set "PATH=%JAVA_HOME%\bin;%PATH%"
) else (
    echo Java found: OK
)

echo [4/6] Checking for APKTool...
if not exist "tools\apktool.jar" (
    echo Downloading APKTool...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13; Invoke-WebRequest -Uri 'https://github.com/iBotPeaches/Apktool/releases/download/v2.10.0/apktool_2.10.0.jar' -OutFile 'tools\apktool.jar' -ErrorAction Stop}" || (
        echo ERROR: Failed to download APKTool
        pause
        exit /b 1
    )
    
    if exist "tools\apktool.jar" (
        echo APKTool downloaded successfully
        
        REM Create apktool.bat wrapper
        echo @echo off > tools\apktool.bat
        echo java -jar "%~dp0apktool.jar" %%* >> tools\apktool.bat
        
        REM Add tools to PATH for this session
        set "PATH=%~dp0tools;%PATH%"
    )
) else (
    echo APKTool found: OK
    set "PATH=%~dp0tools;%PATH%"
)

echo [5/6] Checking for ADB (Android Debug Bridge)...
if not exist "tools\adb.exe" (
    echo Downloading ADB Platform Tools...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13; Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile 'tools\platform-tools.zip' -ErrorAction Stop}" || (
        echo ERROR: Failed to download ADB
        pause
        exit /b 1
    )
    
    if exist "tools\platform-tools.zip" (
        echo Extracting ADB...
        powershell -Command "Expand-Archive -Path 'tools\platform-tools.zip' -DestinationPath 'tools\' -Force"
        copy "tools\platform-tools\adb.exe" "tools\" >nul
        copy "tools\platform-tools\*.dll" "tools\" >nul 2>&1
        rmdir /s /q "tools\platform-tools" >nul 2>&1
        del "tools\platform-tools.zip"
        echo ADB installed successfully
    )
) else (
    echo ADB found: OK
)

echo [6/6] Starting APK Editor Server...
echo.
echo ========================================
echo Server will start on: http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Set environment variables for better performance
set FLASK_ENV=development
set FLASK_DEBUG=1

REM Start the Flask application
"%PYTHON_EXE%" main.py

echo.
echo Server stopped. Press any key to exit...
pause >nul