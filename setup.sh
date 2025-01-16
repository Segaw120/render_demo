#!/bin/bash

# Install system dependencies (for Ubuntu/Debian)
if [ -f /etc/debian_version ]; then
    echo "Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        python3-dev \
        build-essential \
        libffi-dev
fi

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.template .env

# Setup Modal
python modal_setup.py

echo "Setup complete! Please update .env with your credentials." 