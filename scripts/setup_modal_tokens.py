#!/usr/bin/env python3
import os
import subprocess
from dotenv import load_dotenv

def setup_modal_tokens():
    # Load environment variables
    load_dotenv()
    
    # Get tokens from environment
    token_id = os.getenv("MODAL_TOKEN_ID")
    token_secret = os.getenv("MODAL_TOKEN_SECRET")
    
    if not token_id or not token_secret:
        print("Error: Modal tokens not found in environment variables")
        return False
    
    try:
        # Set Modal tokens using CLI
        subprocess.run(
            ["modal", "token", "set", 
             "--token-id", token_id,
             "--token-secret", token_secret],
            check=True
        )
        print("Modal tokens set successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting Modal tokens: {e}")
        return False

if __name__ == "__main__":
    setup_modal_tokens() 