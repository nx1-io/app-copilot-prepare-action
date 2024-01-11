#!/bin/sh -l
set -e

echo "Running..."
python /App/main.py

cd /github/workspace
echo "-----/github/workspace/----"
ls -R