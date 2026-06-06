import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class InstallerThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        try:
            self.status_updated.emit('Creating virtual environment...')
            self.progress_updated.emit(20)
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True, capture_output=True)
            
            self.status_updated.emit('Installing dependencies...')
            self.progress_updated.emit(50)
            
            if sys.platform == 'win32':
                pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
            else:
                pip_path = os.path.join('venv', 'bin', 'pip')
            
            subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True, capture_output=True)
            
            self.status_updated.emit('Setup complete! Starting application...')
            self.progress_updated.emit(100)
            self.finished.emit()
        except Exception as e:
            self.status_updated.emit(f'Error: {str(e)}')

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Portfolio Manager - Setup')
        self.setGeometry(400, 300, 500, 200)
        self.setStyleSheet('background-color: #f0f0f0;')
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel('Stock Portfolio Manager')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.status_label = QLabel('Initializing setup...')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(11)
        self.status_label.setFont(status_font)
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
        self.installer_thread = InstallerThread()
        self.installer_thread.progress_updated.connect(self.update_progress)
        self.installer_thread.status_updated.connect(self.update_status)
        self.installer_thread.finished.connect(self.start_application)
        self.installer_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        self.status_label.setText(status)
    
    def start_application(self):
        import time
        time.sleep(1)
        
        if sys.platform == 'win32':
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:
            python_path = os.path.join('venv', 'bin', 'python')
        
        subprocess.Popen([python_path, 'main.py'])
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec())
