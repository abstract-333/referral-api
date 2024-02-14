from typing import Annotated

from fastapi import APIRouter, Query
from starlette import status

from api.docs import (
    get_user_response,
    update_user_response,
    delete_user_response,
    register_responses,
    register_with_referral_code_responses,
)
from dependencies import CurrentActiveUserDep
from dependencies import UOWDep
from schemas import UserCreate
from schemas import UserUpdate
from schemas.referral_code import ReferralCodeInDB
from schemas.user import UserRead
from services import AuthService
from services import UserService
from services.email import EmailService
from services.referral import ReferralService
from services.referral_code import ReferralCodeService
from settings import settings_obj

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    responses=register_responses,
)
async def register(
    user_data: UserCreate,
    uow: UOWDep,
) -> dict[str, str]:
    await EmailService.verify_email(email=user_data.email)

    auth_service = AuthService()

    if await auth_service.register_new_user(user_data=user_data, uow=uow):
        return {"message": "Account created!!!"}


@user_router.post(
    path="/register/by-referral-code",
    status_code=status.HTTP_201_CREATED,
    responses=register_with_referral_code_responses,
)
async def register_by_referral_code(
    user_data: UserCreate,
    uow: UOWDep,
    referral_code: Annotated[
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
            referral_code=referral_code, uow=uow
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


@user_router.get(
    path="/me",
    response_model=UserRead,
    responses=get_user_response,
)
async def get_user(
    current_user: CurrentActiveUserDep,
):
    return current_user


@user_router.patch(
    path="/update",
    responses=update_user_response,
)
async def patch_user(
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
    updated_user: UserUpdate,
) -> UserRead | None:
    if updated_user.email and updated_user.email != current_user.email:
        await EmailService.verify_email(email=updated_user.email)

    user_service = UserService()

    old_user: UserRead = current_user
    return await user_service.update_user(
        uow=uow, updated_user=updated_user, old_user=old_user
    )


@user_router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_user_response,
)
async def delete_user(
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
) -> None:
    user_service = UserService()
    await user_service.deactivate_user(uow=uow, user_id=str(current_user.id))
