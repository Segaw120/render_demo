import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Environment:
    """Environment configuration"""
    # Environment type
    ENV: str = os.getenv("ENV", "development")
    
    # Redis configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "2025")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Modal configuration
    MODAL_TOKEN_ID: str = os.getenv("MODAL_TOKEN_ID", "")
    MODAL_TOKEN_SECRET: str = os.getenv("MODAL_TOKEN_SECRET", "")
    
    # Service configuration
    POLLING_INTERVAL: int = int(os.getenv("POLLING_INTERVAL", "120"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "5"))
    MAX_BATCH_WAIT: int = int(os.getenv("MAX_BATCH_WAIT", "30"))

env = Environment() 
