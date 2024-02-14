from starlette import status

from .base import HTTPException500

referral_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPException500,
        "description": "Internal Server Error",
    },
}
