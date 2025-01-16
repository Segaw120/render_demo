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

# Prompt for Modal tokens if not in .env
if [ ! -f .env ] || ! grep -q "MODAL_TOKEN_ID" .env; then
    echo "Please enter your Modal token ID (starts with 'ak-'):"
    read modal_token_id
    echo "Please enter your Modal token secret (starts with 'as-'):"
    read modal_token_secret
    
    echo "MODAL_TOKEN_ID=$modal_token_id" >> .env
    echo "MODAL_TOKEN_SECRET=$modal_token_secret" >> .env
fi

# Setup Modal
python scripts/setup_modal_tokens.py
python modal_setup.py

echo "Setup complete! Please update .env with your credentials." 