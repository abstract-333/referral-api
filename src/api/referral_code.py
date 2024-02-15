from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import EmailStr
from starlette import status

from api.docs import (
    get_referral_code_responses,
    get_referral_code_by_email_responses,
    delete_referral_code_responses,
)
from dependencies import UOWDep, CurrentActiveUserDep
from schemas import UserRead
from schemas.referral_code import ReferralCodeRead
from services import AuthService
from services.referral_code import ReferralCodeService
from settings import settings_obj

referral_code_router = APIRouter(
    prefix="/referral-code",
    tags=["Referral Code"],
)


@referral_code_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=get_referral_code_responses,
)
@cache(
    expire=settings_obj.REFERRAL_CODE_EXPIRATION
    // 5,  # Data is cached for set duration in settings
    namespace="referral-code",
)
async def get_referral_code(
    current_user: CurrentActiveUserDep,
    uow: UOWDep,
) -> ReferralCodeRead:
    referral_code_service = ReferralCodeService()
    return await referral_code_service.get_referral_code(
        user_id=current_user.id,
        uow=uow,
    )


@referral_code_router.post(
    path="/{email}",
    status_code=status.HTTP_200_OK,
    responses=get_referral_code_by_email_responses,
)
async def get_referral_code_by_email(
    email: EmailStr,
    uow: UOWDep,
) -> ReferralCodeRead | None:
    auth_service = AuthService()
    user_with_email: UserRead = await auth_service.get_user_by_email(
        email=email, uow=uow
    )
    referral_code_service = ReferralCodeService()
    return await referral_code_service.get_referral_code_by_user_id(
        user_id=user_with_email.id,
        uow=uow,
    )


@referral_code_router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_referral_code_responses,
)
async def delete_referral_code(
    current_user: CurrentActiveUserDep,
    uow: UOWDep,
) -> None:
    referral_code_service = ReferralCodeService()

    await referral_code_service.delete_referral_code_by_user_id(
        user_id=current_user.id,
        uow=uow,
    )
