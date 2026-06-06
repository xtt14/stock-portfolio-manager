@echo off
chcp 65001 >nul
set "ROOT=%~dp0"
cd /d "%ROOT%"

echo Using project root: %ROOT%
if exist "%ROOT%requirements.txt" (
    echo Requirements file content:
    type "%ROOT%requirements.txt"
) else (
    echo Requirements file not found at %ROOT%requirements.txt
)

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
pip install -r "%ROOT%requirements.txt"
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo Creating desktop shortcut...
python "%ROOT%create_shortcut.py"
if errorlevel 1 (
    echo Warning: could not create desktop shortcut.
)

echo Installation complete.
echo You can now launch the app from the desktop shortcut.

echo Press any key to exit...
pause >nul
