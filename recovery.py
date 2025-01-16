import redis
from config import RedisConfig
import logging
import json

logger = logging.getLogger(__name__)

class RecoveryManager:
    def __init__(self, redis_config: RedisConfig):
        self.redis_client = redis.Redis(
            host=redis_config.host,
            port=redis_config.port,
            password=redis_config.password,
            db=redis_config.db,
            decode_responses=True
        )
    
    async def recover_stuck_articles(self):
        """Recover articles stuck in processing"""
        try:
            stuck_articles = self.redis_client.smembers("articles_processing")
            
            for article_id in stuck_articles:
                # Move back to queue
                self.redis_client.lpush("articles_to_analyze", article_id)
                self.redis_client.srem("articles_processing", article_id)
                logger.info(f"Recovered stuck article: {article_id}")
        
        except Exception as e:
            logger.error(f"Error in recovery process: {e}") 