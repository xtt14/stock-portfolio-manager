import os
import subprocess
import sys


def create_windows_shortcut(project_root: str) -> int:
    desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    if not os.path.isdir(desktop):
        print('Desktop folder not found; skipping shortcut creation.')
        return 1

    target = os.path.join(project_root, 'venv', 'Scripts', 'pythonw.exe')
    if not os.path.isfile(target):
        target = os.path.join(project_root, 'venv', 'Scripts', 'python.exe')
    if not os.path.isfile(target):
        print('Python executable not found in the virtual environment.')
        return 1

    shortcut_path = os.path.join(desktop, 'مدير محفظة الأسهم.lnk')
    arguments = os.path.join(project_root, 'main.py')
    working_dir = project_root
    icon_location = target

    powershell_command = (
        '$s=(New-Object -ComObject WScript.Shell).CreateShortcut("' + shortcut_path.replace('"', '\\"') + '"); '
        '$s.TargetPath="' + target.replace('"', '\\"') + '"; '
        '$s.Arguments="' + arguments.replace('"', '\\"') + '"; '
        '$s.WorkingDirectory="' + working_dir.replace('"', '\\"') + '"; '
        '$s.IconLocation="' + icon_location.replace('"', '\\"') + '"; '
        '$s.Save()'
    )

    result = subprocess.run(
        ['powershell', '-NoProfile', '-Command', powershell_command],
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if result.returncode != 0:
        print(result.stdout.strip())
        return result.returncode

    print(f'Created desktop shortcut at {shortcut_path}')
    return 0


def main() -> int:
    project_root = os.path.dirname(os.path.abspath(__file__))
    if os.name != 'nt':
        print('Desktop shortcut creation is supported only on Windows.')
        return 1
    return create_windows_shortcut(project_root)


if __name__ == '__main__':
    sys.exit(main())
