from abc import ABC, abstractmethod


from models.referral import ReferralsOrm
from respositories import SQLAlchemyRepository, AbstractSQLRepository
from schemas.referral import ReferralInDB


class ReferralRepositoryBase(AbstractSQLRepository[ReferralInDB], ABC):
    @abstractmethod
    async def add_referral(self, referral_data: dict) -> None: ...

    @abstractmethod
    async def get_referral(self, **kwargs) -> ReferralInDB | None: ...

    @abstractmethod
    async def delete_referral(self, **kwargs) -> None: ...


class ReferralRepository(SQLAlchemyRepository[ReferralInDB], ReferralRepositoryBase):
    model_cls = ReferralsOrm

    async def add_referral(self, referral_data: dict) -> None:
        await self.add_one(data=referral_data)

    async def get_referral(self, **kwargs) -> ReferralInDB | None:
        tokens: ReferralInDB | None = await self.find_one(**kwargs)
        return tokens

    async def delete_referral(
        self,
        **kwargs,
    ) -> None:
        await self.delete_one(**kwargs)
