@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "ROOT=%~dp0"
set "VENV_DIR=%ROOT%venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
cd /d "%ROOT%"

echo Using project root: %ROOT%
if not exist "%ROOT%requirements.txt" (
    echo Error: requirements.txt not found in %ROOT%
    pause
    exit /b 1
)

echo Detecting Python 3...
set "PY_CMD="
set "PY_ARGS="
call :try_python py -3
if not defined PY_CMD call :try_python python
if not defined PY_CMD call :try_python python3

if not defined PY_CMD (
    echo Python 3 with the venv module was not found on this PC.
    echo Install Python 3 from https://www.python.org/downloads/
    echo During installation, select "Add python.exe to PATH".
    pause
    exit /b 1
)

for /f "tokens=2" %%V in ('"%PY_CMD%" %PY_ARGS% --version 2^>^&1') do set "PY_VERSION=%%V"
echo Using Python %PY_VERSION%: %PY_CMD% %PY_ARGS%

if exist "%VENV_DIR%" if not exist "%VENV_PY%" (
    echo Existing venv folder is incomplete. Recreating it...
    rmdir /s /q "%VENV_DIR%"
    if errorlevel 1 (
        echo Error: could not remove the incomplete venv folder.
        echo Close any running app windows or terminals using this folder, then run setup again.
        pause
        exit /b 1
    )
)

if not exist "%VENV_PY%" (
    echo Creating virtual environment...
    "%PY_CMD%" %PY_ARGS% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Error creating virtual environment.
        echo The selected Python command failed: %PY_CMD% %PY_ARGS% -m venv "%VENV_DIR%"
        pause
        exit /b 1
    )
)

if not exist "%VENV_PY%" (
    echo Error: virtual environment Python was not created at:
    echo %VENV_PY%
    pause
    exit /b 1
)

echo Using virtual environment:
echo %VENV_PY%

echo Upgrading pip in the virtual environment...
"%VENV_PY%" -m pip install --upgrade pip

echo Installing dependencies...
"%VENV_PY%" -m pip install -r "%ROOT%requirements.txt"
if errorlevel 1 (
    echo Error installing dependencies.
    echo Please check your internet connection and Python pip installation.
    pause
    exit /b 1
)

echo Creating desktop shortcut...
"%VENV_PY%" "%ROOT%create_shortcut.py"
if errorlevel 1 (
    echo Warning: could not create desktop shortcut.
)

echo Installation complete.
echo You can now launch the app from the desktop shortcut.

echo Press any key to exit...
pause >nul
endlocal
exit /b 0

:try_python
where "%~1" >nul 2>&1
if errorlevel 1 exit /b 1
"%~1" %~2 -c "import sys, venv; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 exit /b 1
set "PY_CMD=%~1"
set "PY_ARGS=%~2"
exit /b 0
