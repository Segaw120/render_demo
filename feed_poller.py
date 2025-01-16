import uuid
import feedparser
import redis
import json
from datetime import datetime
from typing import Dict, Any
import asyncio
import logging
from config import RedisConfig, FeedConfig, ArticleData, ArticleAnalysis

logger = logging.getLogger(__name__)

class RSSPoller:
    def __init__(self, redis_config: RedisConfig, feed_config: FeedConfig):
        logger.info("Initializing RSS Poller")
        self.redis_client = redis.Redis(
            host=redis_config.host,
            port=redis_config.port,
            password=redis_config.password,
            db=redis_config.db,
            decode_responses=True
        )
        logger.info(f"Connected to Redis at {redis_config.host}:{redis_config.port}")
        self.feed_urls = feed_config.urls
        self.polling_interval = feed_config.polling_interval
        logger.info(f"Configured with {len(feed_config.urls)} feeds, polling every {feed_config.polling_interval} seconds")

    async def save_article(self, article: ArticleData):
        """Save article to Redis in the required format"""
        logger.debug(f"Saving article: {article.title} (ID: {article.id})")
        article_analysis = ArticleAnalysis(article=article)
        
        try:
            # Store as JSON string
            self.redis_client.set(
                self.redis_config.article_key.format(article.id),
                json.dumps(article_analysis.__dict__, default=vars)
            )
            # Add to processing queue
            self.redis_client.lpush(
                self.redis_config.batch_queue,
                article.id
            )
            logger.info(f"Successfully saved article {article.id} to Redis")
        except Exception as e:
            logger.error(f"Failed to save article {article.id}: {str(e)}")
            raise

    async def poll_feeds(self):
        logger.info("Starting RSS feed polling")
        while True:
            for url in self.feed_urls:
                logger.info(f"Polling feed: {url}")
                try:
                    feed = feedparser.parse(url)
                    logger.debug(f"Found {len(feed.entries)} entries in feed {url}")
                    
                    for entry in feed.entries:
                        logger.debug(f"Processing entry: {entry.title}")
                        article = ArticleData(
                            id=str(uuid.uuid4()),
                            title=entry.title,
                            content=entry.get('content', entry.get('summary', '')),
                            source=url,
                            url=entry.link,
                            timestamp=entry.get('published', datetime.now().isoformat())
                        )
                        
                        # Save article using new format
                        await self.save_article(article)

                        # Publish to analysis queue
                        self.redis_client.publish(
                            'articles_to_analyze',
                            article.id
                        )
                        logger.info(f"Published article {article.id} for analysis")

                except Exception as e:
                    logger.error(f"Error polling feed {url}: {str(e)}", exc_info=True)
            
            logger.debug(f"Sleeping for {self.polling_interval} seconds")
            await asyncio.sleep(self.polling_interval)
