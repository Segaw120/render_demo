#!/bin/bash

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.template .env
fi

# Prompt for Modal tokens
echo "Please enter your Modal token ID (starts with 'ak-'):"
read modal_token_id
echo "Please enter your Modal token secret (starts with 'as-'):"
read modal_token_secret

# Update .env file
sed -i "s/MODAL_TOKEN_ID=.*/MODAL_TOKEN_ID=$modal_token_id/" .env
sed -i "s/MODAL_TOKEN_SECRET=.*/MODAL_TOKEN_SECRET=$modal_token_secret/" .env

# Set up Modal tokens
python scripts/setup_modal_tokens.py

echo "Modal configuration updated!" 