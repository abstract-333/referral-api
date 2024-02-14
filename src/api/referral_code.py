from fastapi import APIRouter
from pydantic import EmailStr
from fastapi_cache.decorator import cache
from starlette import status
from dependencies import UOWDep, CurrentActiveUserDep
from schemas.referral_code import ReferralCodeRead
from services.referral_code import ReferralCodeService
from settings import settings_obj

referral_code_router = APIRouter(
    prefix="/referral-code",
    tags=["Referral Code"],
)


@referral_code_router.get(
    path="",
    status_code=status.HTTP_200_OK,
)
@cache(
    expire=settings_obj.REFERRAL_CODE_EXPIRATION
    // 4,  # Data is cached for set duration in settings
    namespace="refferral-code",
)
async def get_referral_code(
    current_user: CurrentActiveUserDep,
    uow: UOWDep,
) -> ReferralCodeRead:
    referral_code_service = ReferralCodeService()
    return await referral_code_service.get_referrel_code(
        user_id=current_user.id,
        uow=uow,
    )


@referral_code_router.post(
    path="/{email}",
    status_code=status.HTTP_200_OK,
)
async def get_referral_code_by_email(
    email: EmailStr,
    uow: UOWDep,
) -> ReferralCodeRead | None:
    referral_code_service = ReferralCodeService()
    return await referral_code_service.get_referral_code_by_email(
        email=email,
        uow=uow,
    )


@referral_code_router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_referral_code(
    current_user: CurrentActiveUserDep,
    uow: UOWDep,
) -> None:
    referral_code_service = ReferralCodeService()

    await referral_code_service.detele_referral_code_by_user_id(
        user_id=current_user.id,
        uow=uow,
    )
