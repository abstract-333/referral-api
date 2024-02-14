from fastapi import APIRouter
from starlette import status

from api.docs import referral_responses
from dependencies import UOWDep, CurrentActiveUserDep
from schemas.user import BaseUser
from services.user import UserService

referral_router = APIRouter(
    prefix="/referral",
    tags=["Referral"],
)


@referral_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=referral_responses,
)
async def get_users_registered_by_referrer_id(
    current_user: CurrentActiveUserDep,
    uow: UOWDep,
) -> list[BaseUser] | None:
    user_service = UserService()
    return await user_service.get_users_registered_by_referrer_id(
        referrer_id=current_user.id,
        uow=uow,
    )
