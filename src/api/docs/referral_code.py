from starlette import status

from exceptions.error_code import ErrorModel, ErrorCode
from .base import HTTPException500

get_referral_code_responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.REFERRAL_CODE_NOT_FOUND: {
                        "summary": "Referral code is not found",
                        "value": {"detail": ErrorCode.REFERRAL_CODE_NOT_FOUND},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPException500,
        "description": "Internal Server Error",
    },
}
get_referral_code_by_email_responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_EXISTS: {
                        "summary": "This email didn't exists",
                        "value": {"detail": ErrorCode.USER_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPException500,
        "description": "Internal Server Error",
    },
}


delete_referral_code_responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.REFERRAL_CODE_NOT_FOUND: {
                        "summary": "Referral code is not found",
                        "value": {"detail": ErrorCode.REFERRAL_CODE_NOT_FOUND},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPException500,
        "description": "Internal Server Error",
    },
}
