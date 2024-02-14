from abc import ABC, abstractmethod

from models import ReferralCodesOrm
from respositories import SQLAlchemyRepository, AbstractSQLRepository
from schemas import ReferralCodeInDB


class ReferralCodeRepositoryBase(AbstractSQLRepository[ReferralCodeInDB], ABC):
    @abstractmethod
    async def add_referral_code(self, referral_data: dict) -> None: ...

    @abstractmethod
    async def get_referral_code(self, **kwargs) -> ReferralCodeInDB | None: ...

    @abstractmethod
    async def delete_referral_code(self, **kwargs) -> None: ...


class ReferralCodeRepository(
    SQLAlchemyRepository[ReferralCodeInDB], ReferralCodeRepositoryBase
):
    model_cls = ReferralCodesOrm

    async def add_referral_code(self, referral_data: dict) -> None:
        await self.add_one(data=referral_data)

    async def get_referral_code(self, **kwargs) -> ReferralCodeInDB | None:
        tokens: ReferralCodeInDB | None = await self.find_one(**kwargs)
        return tokens

    async def delete_referral_code(
        self,
        **kwargs,
    ) -> None:
        await self.delete_one(**kwargs)
