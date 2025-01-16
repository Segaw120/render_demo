import redis
from datetime import datetime, timedelta
from config import RedisConfig
import logging

logger = logging.getLogger(__name__)

class HealthCheck:
    def __init__(self, redis_config: RedisConfig):
        self.redis_client = redis.Redis(
            host=redis_config.host,
            port=redis_config.port,
            password=redis_config.password,
            db=redis_config.db,
            decode_responses=True
        )
    
    async def check_redis_connection(self) -> bool:
        try:
            return self.redis_client.ping()
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            return False
    
    async def check_feed_polling(self) -> bool:
        try:
            last_poll = self.redis_client.get("last_poll_timestamp")
            if not last_poll:
                return False
            
            last_poll_time = datetime.fromisoformat(last_poll)
            return datetime.now() - last_poll_time < timedelta(minutes=5)
        except Exception as e:
            logger.error(f"Feed polling check error: {e}")
            return False
    
    async def check_analysis_worker(self) -> bool:
        try:
            stuck_batches = self.redis_client.scard("articles_processing")
            queue_size = self.redis_client.llen("articles_to_analyze")
            
            return stuck_batches == 0 and queue_size >= 0
        except Exception as e:
            logger.error(f"Analysis worker check error: {e}")
            return False 
