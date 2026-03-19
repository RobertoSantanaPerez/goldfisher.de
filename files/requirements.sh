#!/bin/bash

cd /home/kolyma/Workspace/gold
source /home/kolyma/Workspace/goldfisher.de/files/venv/bin/activate
pip install --upgrade pip
pip install -r /home/kolyma/Workspace/goldfisher.de/files/requirements.txt
deactivate

# end-of-file
