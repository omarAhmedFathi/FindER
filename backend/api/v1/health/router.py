from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.database import get_db
from core.redis import get_redis
from redis.asyncio import Redis

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    status_dict = {"status": "ok", "db": "unknown", "redis": "unknown"}
    
    # DB Check
    try:
        await db.execute(text("SELECT 1"))
        status_dict["db"] = "healthy"
    except Exception:
        status_dict["db"] = "unhealthy"
        status_dict["status"] = "degraded"

    # Redis Check
    try:
        await redis.ping()
        status_dict["redis"] = "healthy"
    except Exception:
        status_dict["redis"] = "unhealthy"
        status_dict["status"] = "degraded"

    return status_dict
