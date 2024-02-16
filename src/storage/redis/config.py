from fastapi import Request, Response

from settings import settings_obj
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool


def get_redis_config():
    pool: ConnectionPool = ConnectionPool.from_url(
        url=f"redis://{settings_obj.REDIS_HOST}:{settings_obj.REDIS_PORT}"
    )
    r = redis.Redis(connection_pool=pool)
    return r


def request_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    return ":".join(
        [
            namespace,
            repr(sorted(request.query_params.items()["current_user"].id)),
        ]
    )
