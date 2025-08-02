
@echo off
echo APKTool Installer for Windows
echo =============================
echo.

echo Creating tools directory...
mkdir tools 2>nul

echo.
echo Checking for Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Java not found!
    echo Please install Java JDK 8 or later from:
    echo https://www.oracle.com/java/technologies/downloads/
    echo.
    echo Alternative: Install OpenJDK from:
    echo https://adoptium.net/
    echo.
    pause
    exit /b 1
)

echo Java found!
java -version
echo.

echo Downloading APKTool...
echo.

echo Downloading apktool wrapper script...
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bitbucket.org/iBotPeaches/apktool/raw/master/scripts/windows/apktool.bat' -OutFile 'tools\apktool.bat' -UseBasicParsing } catch { Write-Host 'Failed to download apktool.bat: ' $_.Exception.Message; exit 1 }"

if %errorlevel% neq 0 (
    echo Failed to download apktool.bat, creating local wrapper...
    echo @echo off > tools\apktool.bat
    echo java -jar "%%~dp0apktool.jar" %%* >> tools\apktool.bat
)

echo Downloading apktool.jar (latest version)...
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $progressPreference = 'silentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/iBotPeaches/Apktool/releases/download/v2.9.3/apktool_2.9.3.jar' -OutFile 'tools\apktool.jar' -UseBasicParsing } catch { Write-Host 'Trying alternative download location...'; try { Invoke-WebRequest -Uri 'https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar' -OutFile 'tools\apktool.jar' -UseBasicParsing } catch { Write-Host 'Failed to download apktool.jar: ' $_.Exception.Message; exit 1 } }"

if %errorlevel% neq 0 (
    echo Failed to download apktool.jar
    echo.
    echo Manual download instructions:
    echo 1. Go to: https://github.com/iBotPeaches/Apktool/releases/latest
    echo 2. Download the latest apktool_X.X.X.jar file
    echo 3. Rename it to apktool.jar and place it in the tools\ folder
    echo.
    pause
    exit /b 1
)

echo.
echo Adding tools to PATH for this session...
set PATH=%CD%\tools;%PATH%

echo.
echo Verifying installation...
if exist "tools\apktool.jar" (
    if exist "tools\apktool.bat" (
        echo SUCCESS: APKTool installed successfully!
        echo Location: %CD%\tools\
        echo.
        echo Testing APKTool...
        tools\apktool.bat --version
        if %errorlevel% equ 0 (
            echo.
            echo ✓ APKTool is working correctly!
            echo.
            echo Installation complete! You can now use the full APK editing features.
            echo.
            echo To test the functionality, run:
            echo python test_apk_functionality.py
        ) else (
            echo.
            echo ⚠ APKTool installed but may not be working correctly.
            echo This could be due to Java configuration issues.
        )
    ) else (
        echo ERROR: apktool.bat not found
    )
) else (
    echo ERROR: apktool.jar not found
)

echo.
echo Note: APKTool PATH is only set for this session.
echo To make it permanent, add %CD%\tools to your system PATH.
echo.
pause
