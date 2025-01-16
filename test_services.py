import pytest
import redis
import asyncio
from feed_poller import RSSPoller
from config import RedisConfig, FeedConfig
from modal_analysis import analyze_article

@pytest.fixture
def redis_client():
    config = RedisConfig()
    client = redis.Redis(
        host=config.host,
        port=config.port,
        password=config.password,
        db=config.db,
        decode_responses=True
    )
    yield client
    client.flushdb()  # Clean up after tests

def test_feed_polling(redis_client):
    config = FeedConfig(
        urls=["https://test-feed.com/rss"],
        polling_interval=5
    )
    poller = RSSPoller(RedisConfig(), config)
    
    # Run poller for a short time
    asyncio.run(asyncio.wait_for(poller.poll_feeds(), timeout=10))
    
    # Check if articles were stored
    keys = redis_client.keys("article:*")
    assert len(keys) > 0

@pytest.mark.asyncio
async def test_article_analysis():
    test_article = {
        "id": "test-uuid",
        "title": "Test Article",
        "content": "This is a test article content.",
        "url": "https://test.com",
        "published_date": "2024-03-20T12:00:00",
        "source": "test",
        "analyzed": False
    }
    
    analysis = await analyze_article.remote(test_article)
    assert analysis.article_id == "test-uuid"
    assert hasattr(analysis, "summary")
    assert hasattr(analysis, "sentiment")
    assert hasattr(analysis, "key_topics") 