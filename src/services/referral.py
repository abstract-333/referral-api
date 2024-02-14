import uuid

from common import IUnitOfWork
from schemas.referral import ReferralCreate


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
