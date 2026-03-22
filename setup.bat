@echo off
REM Setup script for EasyAV antivirus software
REM This script creates a virtual environment and installs dependencies

echo ================================
echo EasyAV - Setup Script (Windows)
echo ================================
echo.
echo This script will check for Python and install required dependencies.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is not installed or not in PATH.
    echo.
    echo Would you like to install Python 3.11 now? (y/n)
    set /p response="Your choice: "

    if /i "!response!"=="y" (
        echo Installing Python 3.11 using winget...
        winget install --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements

        if %errorlevel% neq 0 (
            echo [X] Failed to install Python automatically.
            echo Opening Python download page in your browser...
            start https://www.python.org/downloads/
            echo.
            echo IMPORTANT INSTRUCTIONS:
            echo ----------------------
            echo 1. Download Python 3.11 installer from python.org
            echo 2. Run the installer as Administrator
            echo 3. IMPORTANT: Check "Add Python to PATH" during installation
            echo 4. Complete the installation
            echo 5. RESTART your Command Prompt or PowerShell
            echo 6. Run this setup script again
            echo.
            echo Press any key to exit...
            pause >nul
            exit /b 1
        ) else (
            echo [✓] Python 3.11 installed successfully!
            echo.
            echo IMPORTANT: Please RESTART your Command Prompt or PowerShell
            echo before running this setup script again.
            echo.
            echo Press any key to exit...
            pause >nul
            exit /b 1
        )
    ) else (
        echo [X] Python is required to run EasyAV.
        echo Please install Python 3.7 or higher from: https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% lss 3 (
    echo [X] Python 3.7 or higher is required. Found Python %PYTHON_VERSION%
    echo Please upgrade Python and try again.
    pause
    exit /b 1
)

if %PYTHON_MAJOR%==3 if %PYTHON_MINOR% lss 7 (
    echo [X] Python 3.7 or higher is required. Found Python %PYTHON_VERSION%
    echo Please upgrade Python and try again.
    pause
    exit /b 1
)

echo [OK] Python version check passed!
echo.

REM Install requirements
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Warning: requirements.txt not found
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To run the application, execute:
echo   python main.py
echo.
echo   python main.py
echo.
pause
