@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo Starting application...
python main.py
if errorlevel 1 (
    echo Error running application
    pause
    exit /b 1
)

pause
