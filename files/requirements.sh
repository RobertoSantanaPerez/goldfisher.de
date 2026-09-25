#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"


cd /home/kolyma/Workspace/gold
#source /home/kolyma/Workspace/goldfisher.de/files/venv/bin/activate
source "$SCRIPT_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/Workspace/goldfisher.de/files/requirements.txt"
deactivate

# end-of-file
