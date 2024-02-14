from typing import Final
from redis import Redis
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from starlette import status
from brotli_asgi import BrotliMiddleware
from storage.redis.config import get_redis_config
from views_routers import routers
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # On startup
    redis: Final[Redis] = await get_redis_config()
    FastAPICache.init(backend=RedisBackend(redis=redis), prefix="fastapi-cache")

    yield
    # On shutdown
    await FastAPICache.clear()


app = FastAPI(
    lifespan=app_lifespan,
    title="Referral Project",
    version="0.0.1",
    default_response_class=ORJSONResponse,  # ORJSON is more efficent than default JSON
)

# Using brotli medidleware for compression data in order to increase performance
app.add_middleware(
    middleware_class=BrotliMiddleware,
    quality=6,
    minimum_size=1000,
)


@app.exception_handler(Exception)
async def validation_exception_handler(request, err) -> ORJSONResponse:
    """
    Main exception handler for all routers,
    it returns if none of previous exceptions handlers catching anything
    """
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


for router in routers:
    app.include_router(router=router)
