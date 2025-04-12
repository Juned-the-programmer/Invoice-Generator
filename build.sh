#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies for WeasyPrint
apt-get update
apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate