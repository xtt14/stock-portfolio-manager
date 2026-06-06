import sys
import os
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(PROJECT_ROOT, 'venv')


class InstallerApp:
    def __init__(self, root):
        self.root = root
        root.title('Stock Portfolio Manager Installer')
        root.resizable(False, False)
        root.geometry('620x450')

        frame = tk.Frame(root, padx=15, pady=15)
        frame.pack(fill='both', expand=True)

        title = tk.Label(frame, text='Stock Portfolio Manager Installer', font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(0, 10))

        description = tk.Label(
            frame,
            text='Use this installer to create the virtual environment, install dependencies, and launch the app.',
            wraplength=580,
            justify='left'
        )
        description.pack(pady=(0, 10))

        self.log = scrolledtext.ScrolledText(frame, width=72, height=18, state='disabled', wrap='word')
        self.log.pack(pady=(0, 10), fill='both', expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(fill='x', pady=(0, 5))

        self.install_button = tk.Button(button_frame, text='Install Dependencies', command=self.start_install)
        self.install_button.pack(side='left', padx=(0, 10), pady=5)

        self.launch_button = tk.Button(button_frame, text='Launch Application', command=self.launch_app, state='disabled')
        self.launch_button.pack(side='left', padx=(0, 10), pady=5)

        self.exit_button = tk.Button(button_frame, text='Exit', command=root.quit)
        self.exit_button.pack(side='right', pady=5)

        self.status_label = tk.Label(frame, text='Ready to install.', anchor='w')
        self.status_label.pack(fill='x')

    def write_log(self, message):
        self.log.config(state='normal')
        self.log.insert('end', message + '\n')
        self.log.see('end')
        self.log.config(state='disabled')

    def set_status(self, text):
        self.status_label.config(text=text)

    def start_install(self):
        self.install_button.config(state='disabled')
        self.write_log('Starting installation...')
        self.set_status('Installing...')
        thread = threading.Thread(target=self.install_dependencies, daemon=True)
        thread.start()

    def install_dependencies(self):
        try:
            if not os.path.isdir(VENV_PATH):
                self.write_log('Creating virtual environment...')
                if not self.run_command([sys.executable, '-m', 'venv', VENV_PATH]):
                    raise RuntimeError('Failed to create virtual environment.')

            python_executable = self.get_venv_python()
            self.write_log(f'Using virtual environment Python: {python_executable}')

            self.write_log('Upgrading pip...')
            if not self.run_command([python_executable, '-m', 'pip', 'install', '--upgrade', 'pip']):
                raise RuntimeError('Failed to upgrade pip.')

            self.write_log('Installing required packages...')
            if not self.run_command([python_executable, '-m', 'pip', 'install', '-r', os.path.join(PROJECT_ROOT, 'requirements.txt')]):
                raise RuntimeError('Failed to install dependencies.')

            self.write_log('Installation complete.')
            self.set_status('Installation complete.')
            self.launch_button.config(state='normal')
            self.write_log('Creating desktop shortcut...')
            if self.create_desktop_shortcut():
                self.write_log('Desktop shortcut created successfully.')
            messagebox.showinfo('Success', 'Installation completed successfully.')
        except Exception as exc:
            self.write_log(f'Error: {exc}')
            self.set_status('Installation failed.')
            self.write_log('Desktop shortcut will not be created because install failed.')
            messagebox.showerror('Installation Failed', str(exc))
        finally:
            self.install_button.config(state='normal')

    def get_venv_python(self, use_pythonw=False):
        if os.name == 'nt':
            executable = 'pythonw.exe' if use_pythonw else 'python.exe'
            return os.path.join(VENV_PATH, 'Scripts', executable)
        return os.path.join(VENV_PATH, 'bin', 'python')

    def create_desktop_shortcut(self):
        if os.name != 'nt':
            self.write_log('Desktop shortcut creation skipped: not Windows.')
            return False

        desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
        if not os.path.isdir(desktop):
            self.write_log('Desktop folder not found. Skipping shortcut creation.')
            return False

        shortcut_path = os.path.join(desktop, 'Stock Portfolio Manager.lnk')
        target = self.get_venv_python(use_pythonw=True)
        if not os.path.isfile(target):
            target = self.get_venv_python()

        arguments = os.path.join(PROJECT_ROOT, 'main.py')
        working_dir = PROJECT_ROOT

        powershell_command = (
            '$s=(New-Object -ComObject WScript.Shell).CreateShortcut("' + shortcut_path.replace('"', '\\"') + '"); '
            '$s.TargetPath="' + target.replace('"', '\\"') + '"; '
            '$s.Arguments="' + arguments.replace('"', '\\"') + '"; '
            '$s.WorkingDirectory="' + working_dir.replace('"', '\\"') + '"; '
            '$s.IconLocation="' + target.replace('"', '\\"') + '"; '
            '$s.Save()'
        )

        if self.run_command(['powershell', '-NoProfile', '-Command', powershell_command]):
            self.write_log(f'Created desktop shortcut at {shortcut_path}')
            return True

        fallback_bat = os.path.join(desktop, 'Stock Portfolio Manager.bat')
        try:
            with open(fallback_bat, 'w', encoding='utf-8') as bat_file:
                bat_file.write(
                    f'@echo off\n'
                    f'cd /d "{PROJECT_ROOT}"\n'
                    f'call "{os.path.join(VENV_PATH, "Scripts", "activate.bat")}"\n'
                    f'"{target}" "{os.path.join(PROJECT_ROOT, "main.py")}"\n'
                )
            self.write_log(f'Fallback batch file created at {fallback_bat}')
            return True
        except Exception as bat_exc:
            self.write_log(f'Fallback batch creation failed: {bat_exc}')
            return False

    def run_command(self, command):
        try:
            process = subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False
            )
            self.write_log(process.stdout.strip())
            return process.returncode == 0
        except Exception as exc:
            self.write_log(str(exc))
            return False

    def launch_app(self):
        python_executable = self.get_venv_python()
        if not os.path.isfile(python_executable):
            messagebox.showwarning('Warning', 'Please install dependencies before launching.')
            return

        try:
            subprocess.Popen([python_executable, os.path.join(PROJECT_ROOT, 'main.py')], cwd=PROJECT_ROOT)
            self.write_log('Launching application...')
            self.set_status('Application launched.')
        except Exception as exc:
            self.write_log(f'Launch failed: {exc}')
            messagebox.showerror('Launch Failed', str(exc))


if __name__ == '__main__':
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()
