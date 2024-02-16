import time
import uuid
from fastapi_cache import FastAPICache

from pydantic import PositiveInt

from common import IUnitOfWork
from exceptions.base import (
    ExceptionBadRequest400,
    ExceptionNotFound404,
)
from exceptions.error_code import ErrorCode
from schemas.referral_code import ReferralCodeInDB


class ReferralCodeService:

    @classmethod
    async def _add_referral_code(
        cls,
        create_referral_code: dict,
        uow: IUnitOfWork,
    ):
        async with uow:
            await uow.referral_code.add_one(data=create_referral_code)
            await uow.commit()

    @classmethod
    async def _get_referral_code_by_user_id(
        cls, user_id: uuid.UUID, uow: IUnitOfWork
    ) -> ReferralCodeInDB | None:
        async with uow:
            referral_code: ReferralCodeInDB | None = (
                await uow.referral_code.get_referral_code(user_id=user_id)
            )
            return referral_code

    @classmethod
    async def _get_referral_code(
        cls, referral_code: str, uow: IUnitOfWork
    ) -> ReferralCodeInDB | None:
        async with uow:
            referral_code: ReferralCodeInDB | None = (
                await uow.referral_code.get_referral_code(referral_code=referral_code)
            )
            return referral_code

    @classmethod
    async def _edit_referral_code(
        cls,
        referral_code_data: dict,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.referral_code.edit_one(referral_code_data, user_id=user_id)
            await uow.commit()

    @classmethod
    async def _delete_referral_code(cls, user_id: uuid.UUID, uow: IUnitOfWork) -> None:
        async with uow:
            await uow.referral_code.delete_one(user_id=user_id)
            await uow.commit()

    async def get_referral_code_by_user_id(
        self, user_id: uuid.UUID, uow: IUnitOfWork
    ) -> ReferralCodeInDB | None:
        try:
            referral_code: ReferralCodeInDB | None = (
                await self._get_referral_code_by_user_id(user_id=user_id, uow=uow)
            )
            return referral_code

        except Exception as e:
            raise e

    async def get_referral_code(
        self,
        uow: IUnitOfWork,
        user_id: uuid.UUID,
    ) -> ReferralCodeInDB:
        try:
            old_referral_code: ReferralCodeInDB | None = (
                await self._get_referral_code_by_user_id(
                    user_id=user_id,
                    uow=uow,
                )
            )

            # If referral_code exists in db and it is valid, return it.
            if old_referral_code and not self._is_expired_referral_code(
                valid_until=old_referral_code.valid_until
            ):
                return old_referral_code

            # Delete old referral_code
            await self._delete_referral_code(user_id=user_id, uow=uow)

            # Add new code to db
            await self._add_referral_code(
                create_referral_code={"user_id": user_id}, uow=uow
            )
            created_referral_code: ReferralCodeInDB | None = (
                await self._get_referral_code_by_user_id(
                    user_id=user_id,
                    uow=uow,
                )
            )
            if not created_referral_code:
                raise ExceptionNotFound404(detail=ErrorCode.REFERRAL_CODE_NOT_FOUND)

            return created_referral_code

        except Exception as e:
            raise e

    async def delete_referral_code_by_user_id(
        self, user_id: uuid.UUID, uow: IUnitOfWork
    ) -> None:
        try:
            await FastAPICache.clear(namespace="get_referral_code")
            old_referral_code: ReferralCodeInDB | None = (
                await self._get_referral_code_by_user_id(
                    user_id=user_id,
                    uow=uow,
                )
            )
            if not old_referral_code:
                raise ExceptionNotFound404(detail=ErrorCode.REFERRAL_CODE_NOT_FOUND)

            await self._delete_referral_code(user_id=user_id, uow=uow)

            # Erase cached referral_code

            return None

        except Exception as e:
            raise e

    @staticmethod
    def _is_expired_referral_code(valid_until: PositiveInt) -> bool:
        return valid_until < time.time()

    async def validate_referral_code(
        self,
        referral_code: str,
        uow: IUnitOfWork,
    ) -> ReferralCodeInDB:
        try:
            referral_code: ReferralCodeInDB | None = await self._get_referral_code(
                referral_code=referral_code, uow=uow
            )

            if not referral_code:
                raise ExceptionNotFound404(detail=ErrorCode.REFERRAL_CODE_NOT_FOUND)

            if self._is_expired_referral_code(valid_until=referral_code.valid_until):
                raise ExceptionBadRequest400(detail=ErrorCode.REFERRAL_CODE_INVALID)

            return referral_code

        except Exception as e:
            raise e
