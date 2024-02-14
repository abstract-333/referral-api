import uuid

from common import IUnitOfWork
from exceptions.base import (
    ExceptionBadRequest400,
    ExceptionNotFound404,
)
from exceptions.error_code import ErrorCode
from schemas.referral import ReferralCreate, ReferralInDB


class ReferralService:

    @classmethod
    async def _add_referral(
        cls,
        create_referral: dict,
        uow: IUnitOfWork,
    ):
        async with uow:
            await uow.referral.add_one(data=create_referral)
            await uow.commit()

    @classmethod
    async def _get_referral_by_referrer_id(
        cls,
        referrer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> ReferralInDB | None:
        async with uow:
            referral: ReferralInDB | None = await uow.referral.get_referral_code(
                referrer_id=referrer_id
            )
            return referral

    async def add_referral(
        self,
        referral_id: uuid.UUID,
        referrer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        try:
            create_referral: ReferralCreate = ReferralCreate(
                referrer_id=referrer_id, referral_id=referral_id
            )
            await self._add_referral(
                create_referral=create_referral.model_dump(), uow=uow
            )
            return None

        except Exception as e:
            raise e
