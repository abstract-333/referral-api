from fastapi import APIRouter
from api import (
    auth_router,
    user_router,
    referral_code_router,
    health_router,
    referral_router,
)

routers: list[APIRouter] = [
    auth_router,
    user_router,
    referral_code_router,
    referral_router,
    health_router,
]
