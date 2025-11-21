@echo off
REM EarthCARE Downloader GUI Launcher (Advanced Version)
REM This batch file can be placed anywhere and will find and launch the GUI

REM Set the absolute path to your earthcare_downloader directory
set "EARTHCARE_DIR=d:\onel\python\earthcare_downloader"

REM Check if the directory exists
if not exist "%EARTHCARE_DIR%" (
    echo Error: EarthCARE directory not found at %EARTHCARE_DIR%
    echo Please update the EARTHCARE_DIR variable in this batch file
    pause
    exit /b 1
)

REM Change to the earthcare_downloader directory
cd /d "%EARTHCARE_DIR%"

REM Check if the GUI file exists
if not exist "earthcare_downloader_gui.py" (
    echo Error: earthcare_downloader_gui.py not found in %EARTHCARE_DIR%
    pause
    exit /b 1
)

REM Launch the GUI with Python 3.10
echo Starting EarthCARE Downloader GUI...
py -3.10 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.10 not found. Trying with default python...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Python not found in PATH
        echo Please install Python 3.10 or add Python to your PATH
        pause
        exit /b 1
    )
    python earthcare_downloader_gui.py
) else (
    py -3.10 earthcare_downloader_gui.py
)

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Error occurred while running the application.
    pause
)