#!/bin/bash

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