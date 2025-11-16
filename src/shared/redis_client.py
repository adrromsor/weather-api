from redis.asyncio import Redis

from src.config import settings

_redis_client = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


def get_redis_client() -> Redis:
    return _redis_client
