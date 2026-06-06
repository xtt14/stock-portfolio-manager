from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from ui import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#0f172a'))
    palette.setColor(QPalette.WindowText, QColor('#e2e8f0'))
    palette.setColor(QPalette.Base, QColor('#111827'))
    palette.setColor(QPalette.AlternateBase, QColor('#1e293b'))
    palette.setColor(QPalette.ToolTipBase, QColor('#f8fafc'))
    palette.setColor(QPalette.ToolTipText, QColor('#0f172a'))
    palette.setColor(QPalette.Text, QColor('#e2e8f0'))
    palette.setColor(QPalette.Button, QColor('#2563eb'))
    palette.setColor(QPalette.ButtonText, QColor('#ffffff'))
    palette.setColor(QPalette.Highlight, QColor('#2563eb'))
    palette.setColor(QPalette.HighlightedText, QColor('#ffffff'))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    app.exec_()
