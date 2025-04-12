#!/usr/bin/env bash
set -o errexit

# System dependencies for WeasyPrint
apt-get update
apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2

# Python dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate