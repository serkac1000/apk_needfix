@echo off
title APK Editor - Auto Start Server
echo ============================================================
echo APK Editor - Auto Start Server
echo ============================================================
echo Starting server at http://127.0.0.1:5000
echo Browser will open automatically...
echo ============================================================
echo.

REM Set Python path
set PYTHON_PATH=C:\Users\serka\AppData\Local\Programs\Python\Python312\python.exe

REM Check if Python is available at the specified path
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    echo Trying system Python...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Error: Python is not installed or not in PATH
        echo Please install Python 3.11+ and try again
        pause
        exit /b 1
    )
    set PYTHON_PATH=python
)

REM Start the auto server
"%PYTHON_PATH%" auto_start_server.py

echo.
echo Server stopped.
pause