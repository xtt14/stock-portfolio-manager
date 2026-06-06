#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    python3 installer.py
else
    ./venv/bin/python3 main.py
fi
