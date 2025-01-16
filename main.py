import asyncio
from config import RedisConfig, FeedConfig, ModalConfig
from feed_poller import RSSPoller
from modal_analysis import analysis_worker
from utils.logging_config import setup_logging
from env_config import env

async def main():
    # Setup logging
    setup_logging(env.ENV)
    
    # Initialize services
    redis_config = RedisConfig()
    feed_config = FeedConfig()
    
    # Start RSS Poller
    poller = RSSPoller(redis_config, feed_config)
    
    # Start Modal Analysis Worker
    analysis_task = asyncio.create_task(
        analysis_worker(redis_config)
    )
    
    # Start Feed Polling
    polling_task = asyncio.create_task(
        poller.poll_feeds()
    )
    
    try:
        await asyncio.gather(polling_task, analysis_task)
    except Exception as e:
        logger.error(f"Service error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 