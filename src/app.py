import sentry_sdk
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin
from starlette import status
from admin import AdminAuth
from models import async_engine, async_session_maker
from settings import settings_obj
from views_routers import routers, views

sentry_sdk.init(
    dsn=settings_obj.SENTRY_URL,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
app = FastAPI(
    title="Tishreen University",
    version="0.0.2",
    default_response_class=ORJSONResponse,
)

# app.add_middleware(HotReloadMiddleware)
app.add_middleware(
    middleware_class=BrotliMiddleware,
    quality=6,
    minimum_size=1000,
)


@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    """
    Main exception handler for all routers,
    it returns if none of previous exceptions handlers catching anything
    """
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    sentry_sdk.capture_message(f"{base_error_message}. Detail: {err}")
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


authentication_backend = AdminAuth(secret_key=settings_obj.JWT_SECRET_KEY)
admin = Admin(
    app=app,
    authentication_backend=authentication_backend,
    engine=async_engine,
    session_maker=async_session_maker,
    title="Tishreen University",
    debug=True,
)


for view in views:
    admin.add_view(view)
for router in routers:
    app.include_router(router)
