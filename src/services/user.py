import uuid
from typing import Any, Tuple

from common import IUnitOfWork
from exceptions import (
    ExceptionNotFound404,
    ExceptionNotAcceptable406,
)
from exceptions.error_code import ErrorCode
from schemas import (
    UserRead,
    UserUpdate,
)
from schemas.user import BaseUser


class UserService:
    @classmethod
    async def get_user(
        cls,
        uow: IUnitOfWork,
        **kwargs,
    ) -> UserRead | None:
        """Get user by **kwargs"""
        async with uow:
            user: UserRead | None = await uow.user.get_user(**kwargs)
            return user

    @classmethod
    async def _get_users_registered_by_referrer_id(
        cls,
        referrer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> Tuple[BaseUser] | None:
        async with uow:
            users_joined_by_referrer_id: Tuple[BaseUser] | None = (
                await uow.user.join_users_by_referral_id(referrer_id=referrer_id)
            )

            return users_joined_by_referrer_id

    @classmethod
    async def edit_user(
        cls,
        uow: IUnitOfWork,
        user_data: dict,
        **kwargs,
    ) -> None:
        """Edit user by **kwargs"""
        async with uow:
            await uow.user.edit_user(user_data=user_data, **kwargs)
            await uow.commit()

    async def update_user(
        self,
        updated_user: UserUpdate,
        old_user: UserRead,
        uow: IUnitOfWork,
    ) -> UserRead | None:
        if updated_user == old_user:
            return old_user

        user_id: uuid.UUID = old_user.id
        user_from_db: UserRead | None = await self.get_user(uow=uow, id=user_id)

        if user_from_db is None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        if updated_user.email and updated_user.email != old_user.email:
            user_same_email: UserRead | None = await self.get_user(
                uow=uow,
                email=updated_user.email,
            )

            if user_same_email is not None:
                raise ExceptionNotAcceptable406(detail=ErrorCode.EMAIL_ALREADY_EXISTS)

        updated_user_dict: dict[str, Any] = updated_user.model_dump(
            exclude_unset=True, exclude_none=True, exclude_defaults=True
        )
        await self.edit_user(uow=uow, user_data=updated_user_dict, id=user_id)
        returned_user: UserRead | None = await self.get_user(id=user_id, uow=uow)

        if not returned_user:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        return await self.get_user(uow=uow, id=user_id)

    async def deactivate_user(
        self,
        user_id: str,
        uow: IUnitOfWork,
    ) -> None:
        user_from_db: UserRead | None = await self.get_user(uow=uow, id=user_id)

        # Ensures that user is existed, and raise exception otherwise
        if user_from_db is not None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        await self.edit_user(
            uow=uow,
            user_data={"is_active": False},
            id=user_id,
        )

    async def get_users_registered_by_referrer_id(
        self, referrer_id: uuid.UUID, uow: IUnitOfWork
    ) -> Tuple[BaseUser] | None:
        try:
            registered_by_referrer_id: Tuple[BaseUser] | None = (
                await self._get_users_registered_by_referrer_id(
                    referrer_id=referrer_id, uow=uow
                )
            )
            return registered_by_referrer_id

        except Exception as e:
            raise e
