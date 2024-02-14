from typing import Annotated
from fastapi import APIRouter, Query
from starlette import status

from dependencies import UOWDep, OAuth2Dep
from schemas import AccessRefreshTokens, UserCreate
from schemas.referral_code import ReferralCodeInDB
from schemas.user import UserRead
from services import AuthService
from services.email import EmailService
from services.referral import ReferralService
from services.referral_code import ReferralCodeService
from .docs import sign_up_responses
from .docs.auth import sign_in_response, sign_out_response, get_tokens_response
from settings import settings_obj

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post(
    path="/sign-up",
    status_code=status.HTTP_201_CREATED,
    responses=sign_up_responses,
)
async def sign_up(
    user_data: UserCreate,
    uow: UOWDep,
) -> dict[str, str]:
    await EmailService.verify_email(email=user_data.email)

    auth_service = AuthService()

    if await auth_service.register_new_user(user_data=user_data, uow=uow):
        return {"message": "Account created!!!"}


@auth_router.post(
    path="/sign-up/by-referral-code",
    status_code=status.HTTP_201_CREATED,
    responses=sign_up_responses,
)
async def sign_up_by_referral_code(
    user_data: UserCreate,
    uow: UOWDep,
    refferal_code: Annotated[
        str | None,
        Query(
            min_length=settings_obj.NANO_ID_LENGTH,
            max_length=settings_obj.NANO_ID_LENGTH,
        ),
    ],
) -> dict[str, str]:
    await EmailService.verify_email(email=user_data.email)

    auth_service = AuthService()
    referral_code_service = ReferralCodeService()
    referral_service = ReferralService()
    validated_referral_code: ReferralCodeInDB = (
        await referral_code_service.validate_referral_code(
            referral_code=refferal_code, uow=uow
        )
    )
    await auth_service.register_new_user(user_data=user_data, uow=uow)
    created_user: UserRead = await auth_service.get_user_by_email(
        email=user_data.email, uow=uow
    )
    await referral_service.add_referral(
        referral_id=created_user.id,
        referrer_id=validated_referral_code.user_id,
        uow=uow,
    )
    return {"message": "Account created!!!"}


@auth_router.post(
    path="/sign-in",
    response_model=AccessRefreshTokens,
    responses=sign_in_response,
)
async def sign_in(
    uow: UOWDep,
    form_data: OAuth2Dep,
) -> AccessRefreshTokens:
    auth_service = AuthService(is_active=True)
    return await auth_service.authenticate_user(
        email=form_data.username, password=form_data.password, uow=uow
    )


@auth_router.post(
    path="/get-tokens",
    response_model=AccessRefreshTokens,
    status_code=status.HTTP_200_OK,
    responses=get_tokens_response,
)
async def get_access_refresh_tokens(
    uow: UOWDep,
    refresh_token: str,
) -> AccessRefreshTokens:
    auth_service = AuthService(is_active=True)
    refresh_token_string: bytes = bytes(refresh_token, "utf-8")
    return await auth_service.create_tokens(refresh_token=refresh_token_string, uow=uow)


@auth_router.post(
    path="/sign-out",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=sign_out_response,
)
async def sign_out(
    uow: UOWDep,
    refresh_token: str,
) -> None:
    auth_service = AuthService(is_active=True)
    refresh_token_string: bytes = bytes(refresh_token, "utf-8")
    await auth_service.revoke_token(refresh_token=refresh_token_string, uow=uow)
