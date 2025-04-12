#!/usr/bin/env bash
set -o errexit

# System dependencies for WeasyPrint
apt-get update
apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2
echo "System Dependency successfully"

# Python dependencies
pip install -r requirements.txt
echo "Requirements Done"

# Database setup
python manage.py migrate
echo "Build completed successfully"