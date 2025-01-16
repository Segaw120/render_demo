from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import logging
import sys

# Configure logging
def setup_logging(level=logging.INFO):
    """Configure logging with a standard format"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('rss_poller.log')
        ]
    )

# Call setup_logging at module level
setup_logging()

@dataclass
class ModalConfig:
    """Modal-specific configuration"""
    token_id: str = ""  # Add your Modal token ID here
    token_secret: str = ""  # Add your Modal token secret here
    model_name: str = "curiousily/Llama-3-8B-Instruct-Finance-RAG"
    gpu_config: str = "T4"  # Modal GPU configuration
    model_version: str = "1.0"
    batch_size: int = 5  # Number of articles to analyze in one batch
    max_batch_wait: int = 30  # Maximum seconds to wait before processing incomplete batch
    container_idle_timeout: int = 300  # Keep containers warm for 5 minutes
    keep_warm: int = 2  # Keep 2 warm containers ready

@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    password: str = "2025"  # Updated per requirements
    db: int = 0
    # Redis key patterns
    article_key: str = "article_data:{}"  # Format with article_id
    analysis_key: str = "analysis:{}"     # Format with article_id
    batch_queue: str = "articles_to_analyze"
    processing_set: str = "articles_processing"
    batch_lock: str = "batch_lock"
    batch_timeout: int = 60  # Seconds before considering a batch stuck

@dataclass
class FeedConfig:
    urls: List[str] = field(default_factory=lambda: [
        "https://ambcrypto.com/feed/"
    ])
    polling_interval: int = 120  # Updated to 120 seconds per requirements

@dataclass
class ArticleData:
    """Article data structure"""
    id: str
    title: str
    content: str
    source: str
    url: str
    timestamp: str

@dataclass
class RiskAssessment:
    level: str
    reason: str

@dataclass
class StructuredAnalysis:
    summary: str
    market_impact: str
    trading_ideas: List[str]
    key_assets: List[str]
    risk: RiskAssessment

@dataclass
class AnalysisData:
    """Analysis data structure"""
    structured_analysis: StructuredAnalysis
    model: str
    version: str
    processing_time: float

@dataclass
class ArticleAnalysis:
    """Combined article and analysis data structure"""
    article: ArticleData
    analysis: Optional[AnalysisData] = None
