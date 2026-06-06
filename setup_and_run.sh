#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    ./venv/bin/python3 -m pip install --upgrade pip
    ./venv/bin/python3 -m pip install -r requirements.txt
fi

echo "Installation complete. Run the app from the desktop shortcut or execute ./venv/bin/python3 main.py"
