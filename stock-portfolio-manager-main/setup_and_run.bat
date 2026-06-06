@echo off
chcp 65001 >nul
cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel% neq 0 (
    start "" python "%~dp0installer.py"
) else (
    start "" pythonw "%~dp0installer.pyw"
)
exit /b
