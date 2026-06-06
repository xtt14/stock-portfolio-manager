from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from ui import MainWindow
import os
from settings import get_theme


def load_fonts(app):
    """Load fonts from assets/fonts and return the primary family name if loaded."""
    fonts_dir = os.path.join(os.path.dirname(__file__), 'assets', 'fonts')
    if not os.path.isdir(fonts_dir):
        return None

    for fname in os.listdir(fonts_dir):
        if not fname.lower().endswith(('.ttf', '.otf')):
            continue
        path = os.path.join(fonts_dir, fname)
        try:
            id_ = QFontDatabase.addApplicationFont(path)
            if id_ != -1:
                families = QFontDatabase.applicationFontFamilies(id_)
                if families:
                    return families[0]
        except Exception:
            continue
    return None


def load_stylesheet(app, variant='dark'):
    base = os.path.join(os.path.dirname(__file__), 'assets')
    filename = 'style_dark.qss' if variant == 'dark' else 'style_light.qss'
    qss_path = os.path.join(base, filename)
    if os.path.exists(qss_path):
        try:
            with open(qss_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication([])
    # load saved theme preference
    try:
        theme_pref = get_theme()
    except Exception:
        theme_pref = 'dark'
    # try to set application font to AlJazeera if available (fallbacks will apply)
    # attempt to load bundled fonts and set app font to bold weight
    try:
        family = load_fonts(app)
        if family:
            font = QFont(family, 11, QFont.Bold)
        else:
            font = QFont('', 11, QFont.Bold)
        font.setWeight(QFont.Bold)
        app.setFont(font)
    except Exception:
        pass

    load_stylesheet(app, variant=theme_pref)
    window = MainWindow()
    window.show()
    app.exec_()
