import modal
from env_config import env

def setup_modal():
    """Set up Modal authentication and configuration"""
    try:
        modal.setup(
            token_id=env.MODAL_TOKEN_ID,
            token_secret=env.MODAL_TOKEN_SECRET
        )
        return True
    except Exception as e:
        print(f"Error setting up Modal: {e}")
        return False

if __name__ == "__main__":
    setup_modal() 
