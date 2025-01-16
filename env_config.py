import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass

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
    MODAL_TOKEN_ID: Optional[str] = os.getenv("MODAL_TOKEN_ID")
    MODAL_TOKEN_SECRET: Optional[str] = os.getenv("MODAL_TOKEN_SECRET")
    
    # Render configuration
    RENDER_API_KEY: Optional[str] = os.getenv("RENDER_API_KEY")
    RENDER_SERVICE_ID: Optional[str] = os.getenv("RENDER_SERVICE_ID")
    
    # Service configuration
    POLLING_INTERVAL: int = int(os.getenv("POLLING_INTERVAL", "120"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "5"))
    MAX_BATCH_WAIT: int = int(os.getenv("MAX_BATCH_WAIT", "30"))
    
    @property
    def is_production(self) -> bool:
        return self.ENV == "production"
    
    def validate(self):
        """Validate environment configuration"""
        # Basic required variables
        basic_vars = ["REDIS_PASSWORD"]
        
        # Modal-specific variables
        modal_vars = ["MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET"]
        
        # Production-only variables
        prod_vars = ["RENDER_API_KEY", "RENDER_SERVICE_ID"]
        
        # Check basic variables
        missing = [var for var in basic_vars if not getattr(self, var)]
        if missing:
            raise ConfigurationError(f"Missing required variables: {', '.join(missing)}")
        
        # Check Modal variables
        missing_modal = [var for var in modal_vars if not getattr(self, var)]
        if missing_modal:
            raise ConfigurationError(f"Missing Modal configuration: {', '.join(missing_modal)}")
        
        # Check production variables
        if self.is_production:
            missing_prod = [var for var in prod_vars if not getattr(self, var)]
            if missing_prod:
                raise ConfigurationError(
                    f"Missing production configuration: {', '.join(missing_prod)}"
                )
        
        return self

env = Environment().validate() 