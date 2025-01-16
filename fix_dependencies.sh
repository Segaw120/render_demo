#!/bin/bash

# Fix missing dependencies
sudo apt-get update
sudo apt-get install -y python3-dev build-essential libffi-dev
pip install --no-cache-dir -r requirements.txt 