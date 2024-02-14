from typing import Final

from redis import asyncio as aioredis, Redis
from settings import settings_obj


async def get_redis_config() -> Redis:
    redis: Final[Redis] = await aioredis.from_url(
        url=f"redis://{settings_obj.REDIS_HOST}:{settings_obj.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    return redis
