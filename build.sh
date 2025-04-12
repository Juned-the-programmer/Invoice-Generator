#!/usr/bin/env bash
set -o errexit
set -x  # Enable command echoing

echo "=== STARTING BUILD ==="
pwd
ls -la

echo "Installing system dependencies..."
apt-get update
apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "=== BUILD COMPLETE ==="