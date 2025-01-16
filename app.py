from fastapi import FastAPI, HTTPException
from health import HealthCheck
from config import RedisConfig

app = FastAPI()
health_check = HealthCheck(RedisConfig())

@app.get("/health")
async def health():
    redis_health = await health_check.check_redis_connection()
    feed_health = await health_check.check_feed_polling()
    analysis_health = await health_check.check_analysis_worker()
    
    if not all([redis_health, feed_health, analysis_health]):
        raise HTTPException(status_code=503, detail="Service unhealthy")
    
    return {"status": "healthy"} 
