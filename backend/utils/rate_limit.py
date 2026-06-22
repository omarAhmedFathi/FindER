from fastapi import Request, HTTPException
from core.redis import get_redis
from fastapi import Depends

async def rate_limiter(request: Request, redis=Depends(get_redis)):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    current_count = await redis.get(key)
    if current_count and int(current_count) >= 100:
        raise HTTPException(status_code=429, detail="Too many requests. Limit is 100 per minute.")
    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, 60)
    await pipe.execute()
