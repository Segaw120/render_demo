import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TokenValidator:
    @staticmethod
    def validate_modal_token(token_id: Optional[str], token_secret: Optional[str]) -> bool:
        """Validate Modal token format"""
        if not token_id or not token_secret:
            return False
            
        # Modal token format validation
        token_id_pattern = r'^ak-[a-zA-Z0-9]{16}$'
        token_secret_pattern = r'^as-[a-zA-Z0-9]{16}$'
        return (
            bool(re.match(token_id_pattern, token_id)) and
            bool(re.match(token_secret_pattern, token_secret))
        )
    
    @staticmethod
    def validate_render_token(api_key: Optional[str], service_id: Optional[str]) -> bool:
        """Validate Render token format"""
        if not api_key or not service_id:
            return False
            
        # Render API key format validation
        api_key_pattern = r'^rnd_[a-zA-Z0-9]{32}$'
        service_id_pattern = r'^srv-[a-zA-Z0-9]{16}$'
        
        return (
            bool(re.match(api_key_pattern, api_key)) and
            bool(re.match(service_id_pattern, service_id))
        ) 