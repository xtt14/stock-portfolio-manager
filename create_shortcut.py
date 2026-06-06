import subprocess
import os
import sys
import platform

def create_desktop_shortcut():
    system = platform.system()
    
    if system == 'Windows':
        create_windows_shortcut()
    elif system == 'Darwin':
        create_mac_shortcut()
    elif system == 'Linux':
        create_linux_shortcut()

def create_windows_shortcut():
    import win32com.client
    
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop_path, 'Stock Portfolio Manager.lnk')
    script_path = os.path.abspath('run.bat')
    
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.save()
    
    print(f'تم إنشاء الاختصار على سطح المكتب: {shortcut_path}')

def create_mac_shortcut():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    app_path = os.path.join(desktop_path, 'Stock Portfolio Manager')
    script_path = os.path.abspath('run.sh')
    
    os.makedirs(app_path, exist_ok=True)
    
    with open(os.path.join(app_path, 'run.sh'), 'w') as f:
        f.write(f'#!/bin/bash\ncd "{os.path.dirname(script_path)}"\npython3 main.py')
    
    os.chmod(os.path.join(app_path, 'run.sh'), 0o755)
    
    print(f'تم إنشاء الاختصار على سطح المكتب: {app_path}')

def create_linux_shortcut():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop_path, 'stock-portfolio.desktop')
    script_path = os.path.abspath('run.sh')
    
    desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Stock Portfolio Manager
Exec={script_path}
Icon=application-x-executable
Terminal=false
Categories=Utility;
'''
    
    with open(shortcut_path, 'w') as f:
        f.write(desktop_content)
    
    os.chmod(shortcut_path, 0o755)
    
    print(f'تم إنشاء الاختصار على سطح المكتب: {shortcut_path}')

if __name__ == '__main__':
    try:
        create_desktop_shortcut()
    except Exception as e:
        print(f'خطأ: {e}')
