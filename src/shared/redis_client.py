from redis.asyncio import Redis

from src.config import settings

_redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


def get_redis_client() -> Redis:
    return _redis_client
