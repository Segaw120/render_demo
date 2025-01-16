import modal
import redis
import json
from datetime import datetime
from typing import Dict, List
from config import (RedisConfig, ModalConfig, ArticleAnalysis,
                   AnalysisData, StructuredAnalysis, RiskAssessment)
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
import logging
import asyncio

logger = logging.getLogger(__name__)

app = modal.App("article-analysis")

# Update image to include the specific model requirements
image = (
    modal.Image.debian_slim()
    .apt_install(["python3-dev", "build-essential", "libffi-dev"])
    .pip_install(
        "redis",
        "transformers>=4.34.0",
        "torch>=2.0.0",
        "accelerate",
        "sentencepiece",
        "nltk"
    )
)

@app.function(
    image=image,
    gpu=ModalConfig.gpu_config,
    container_idle_timeout=ModalConfig.container_idle_timeout,
    keep_warm=ModalConfig.keep_warm
)
def analyze_articles_batch(articles_data: List[Dict]) -> List[AnalysisData]:
    """
    Analyze a batch of articles using Llama-3-8B-Instruct-Finance model
    """
    logger.info(f"Starting batch analysis for {len(articles_data)} articles")
    start_time = time.time()

    analyses = []
    
    try:
        # Load model and tokenizer once for the batch
        logger.debug("Loading model and tokenizer")
        model_name = ModalConfig.model_name
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        logger.debug("Model loaded successfully")

        for article_data in articles_data:
            logger.debug(f"Analyzing article: {article_data['id']}")
            
            prompt = f"""Analyze the following financial article and provide:
1. A brief summary
2. Market impact assessment
3. Potential trading ideas
4. Key assets mentioned
5. Risk assessment (High/Medium/Low) with explanation

Article: {article_data['content']}

Analysis:"""

            # Generate analysis
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(
                **inputs,
                max_length=1024,
                temperature=0.7,
                num_return_sequences=1
            )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            try:
                lines = response.split('\n')
                summary = lines[0]
                market_impact = lines[1] if len(lines) > 1 else ""
                trading_ideas = [t.strip() for t in lines[2].split(',')] if len(lines) > 2 else []
                key_assets = [a.strip() for a in lines[3].split(',')] if len(lines) > 3 else []
                risk_assessment = lines[4].split(':') if len(lines) > 4 else ["Medium", "Unknown"]
                logger.debug("Successfully parsed model output")
                
                structured_analysis = StructuredAnalysis(
                    summary=summary,
                    market_impact=market_impact,
                    trading_ideas=trading_ideas,
                    key_assets=key_assets,
                    risk=RiskAssessment(
                        level=risk_assessment[0],
                        reason=risk_assessment[1]
                    )
                )

                analysis = AnalysisData(
                    structured_analysis=structured_analysis,
                    model=ModalConfig.model_name,
                    version=ModalConfig.model_version,
                    processing_time=time.time() - start_time
                )
                analyses.append(analysis)
                
            except Exception as e:
                logger.error(f"Error parsing article {article_data['id']}: {e}", exc_info=True)
                
    except Exception as e:
        logger.error(f"Error in batch processing: {e}", exc_info=True)

    total_time = time.time() - start_time
    logger.info(f"Batch analysis completed in {total_time:.2f} seconds")
    return analyses

@app.function(image=image)
async def analysis_worker(redis_config: RedisConfig):
    """
    Worker that listens for new articles and processes them in batches
    """
    logger.info("Starting analysis worker")
    redis_client = redis.Redis(
        host=redis_config.host,
        port=redis_config.port,
        password=redis_config.password,
        db=redis_config.db,
        decode_responses=True
    )
    logger.info("Connected to Redis")
    
    async def process_batch():
        # Try to acquire batch lock
        if not redis_client.set(redis_config.batch_lock, "1", 
                               nx=True, ex=redis_config.batch_timeout):
            return
        
        try:
            # Get batch of articles
            article_ids = redis_client.lrange(
                redis_config.batch_queue, 0, ModalConfig.batch_size - 1
            )
            
            if not article_ids:
                return
            
            # Move articles to processing set
            redis_client.sadd(redis_config.processing_set, *article_ids)
            redis_client.ltrim(redis_config.batch_queue, len(article_ids), -1)
            
            # Get article data
            articles_data = []
            for article_id in article_ids:
                data = redis_client.get(redis_config.article_key.format(article_id))
                if data:
                    articles_data.append(json.loads(data))
            
            # Process batch
            analyses = await analyze_articles_batch.remote(articles_data)
            
            # Store results
            for article_id, analysis in zip(article_ids, analyses):
                redis_client.set(
                    redis_config.analysis_key.format(article_id),
                    json.dumps(analysis.__dict__, default=vars)
                )
            
            # Remove from processing set
            redis_client.srem(redis_config.processing_set, *article_ids)
            
        finally:
            redis_client.delete(redis_config.batch_lock)
    
    while True:
        try:
            # Check queue length
            queue_len = redis_client.llen(redis_config.batch_queue)
            
            if queue_len >= ModalConfig.batch_size:
                await process_batch()
            elif queue_len > 0:
                # Wait for more articles or timeout
                await asyncio.sleep(ModalConfig.max_batch_wait)
                await process_batch()
            else:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in batch processing: {e}", exc_info=True)
            await asyncio.sleep(5)  # Wait before retrying
