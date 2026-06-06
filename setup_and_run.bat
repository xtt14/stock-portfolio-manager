@echo off
cd /d "%~dp0"
if not exist "venv" (
    python installer.py
) else (
    venv\Scripts\python.exe main.py
)
