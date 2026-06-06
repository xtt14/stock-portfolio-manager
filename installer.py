import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class OfflineInstallerThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def run(self):
        try:
            self.status_updated.emit('جاري إنشاء بيئة افتراضية... / Creating virtual environment...')
            self.progress_updated.emit(10)
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True, capture_output=True)
            
            self.status_updated.emit('جاري تحميل المكتبات من الملف المحلي... / Installing from local files...')
            self.progress_updated.emit(40)
            
            if sys.platform == 'win32':
                pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
            else:
                pip_path = os.path.join('venv', 'bin', 'pip')
            
            # محاولة التثبيت بدون الإنترنت أولاً من مجلد packages إذا كان موجوداً
            if os.path.exists('packages'):
                self.status_updated.emit('جاري تثبيت المكتبات من المجلد المحلي... / Installing from local packages folder...')
                subprocess.run([pip_path, 'install', '--no-index', '--find-links=./packages', '-r', 'requirements.txt'], 
                             check=True, capture_output=True)
            else:
                # محاولة التثبيت العادي
                subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True, capture_output=True)
            
            self.status_updated.emit('تم الانتهاء! جاري تشغيل التطبيق... / Setup complete! Starting application...')
            self.progress_updated.emit(100)
            self.finished.emit(True)
        except Exception as e:
            error_msg = f'خطأ / Error: {str(e)}'
            self.status_updated.emit(error_msg)
            self.progress_updated.emit(0)
            self.finished.emit(False)

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Portfolio Manager - Setup')
        self.setGeometry(400, 300, 600, 250)
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
        
        subtitle = QLabel('مدير محفظة الأسهم')
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        self.status_label = QLabel('جاري البدء... / Initializing setup...')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
        self.installer_thread = OfflineInstallerThread()
        self.installer_thread.progress_updated.connect(self.update_progress)
        self.installer_thread.status_updated.connect(self.update_status)
        self.installer_thread.finished.connect(self.on_finished)
        self.installer_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        self.status_label.setText(status)
    
    def on_finished(self, success):
        import time
        time.sleep(1)
        
        if success:
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
