#!/bin/bash

cd /home/kolyma/Workspace/goldfisher.de/files || exit 1
rm -f /run/flaskapp.sock
./venv/bin/gunicorn --workers 4 --threads 2 --bind unix:/run/flaskapp.sock --umask 007 --timeout 60 --bind 127.0.0.1:8005 app:app

# end-of-file 