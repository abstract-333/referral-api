from fastapi import APIRouter, BackgroundTasks
from starlette import status
from starlette.responses import HTMLResponse

from api.docs import (
    get_user_response,
    update_user_response,
    delete_user_response,
)
from dependencies import UOWDep, CurrentActiveUserDep
from schemas import UserRead, UserUpdate
from services import UserService
from services.email import EmailService

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


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
