import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.json')

DEFAULTS = {
    'theme': 'dark'
}


def _read_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULTS.copy()
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return DEFAULTS.copy()
            return {**DEFAULTS, **data}
    except Exception:
        return DEFAULTS.copy()


def _write_settings(data: dict):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_theme():
    return _read_settings().get('theme', DEFAULTS['theme'])


def set_theme(theme: str):
    s = _read_settings()
    s['theme'] = theme
    _write_settings(s)
