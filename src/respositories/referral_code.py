from abc import ABC, abstractmethod
from typing import Tuple

from pydantic import EmailStr
from sqlalchemy import Select, select

from models import ReferralCodesOrm
from models.user import UsersOrm
from respositories import SQLAlchemyRepository, AbstractSQLRepository
from schemas import ReferralCodeInDB


class ReferralCodeRepositoryBase(AbstractSQLRepository[ReferralCodeInDB], ABC):
    @abstractmethod
    async def add_referral_code(self, referral_data: dict) -> None: ...

    @abstractmethod
    async def get_referral_code(self, **kwargs) -> ReferralCodeInDB | None: ...

    @abstractmethod
    async def delete_referral_code(self, **kwargs) -> None: ...

    @abstractmethod
    async def get_referral_code_by_email(
        self, email: EmailStr
    ) -> ReferralCodeInDB | None: ...


class ReferralCodeRepository(
    SQLAlchemyRepository[ReferralCodeInDB], ReferralCodeRepositoryBase
):
    model_cls = ReferralCodesOrm

    async def add_referral_code(self, referral_data: dict) -> None:
        await self.add_one(data=referral_data)

    async def get_referral_code(self, **kwargs) -> ReferralCodeInDB | None:
        tokens: ReferralCodeInDB | None = await self.find_one(**kwargs)
        return tokens

    async def get_referral_code_by_email(
        self, email: EmailStr
    ) -> ReferralCodeInDB | None:
        query: Select[Tuple[ReferralCodesOrm]] = (
            select(ReferralCodesOrm)
            .join(UsersOrm)
            .filter(UsersOrm.email == email)
            .limit(1)
        )
        result = await self.session.execute(query)
        result = result.one_or_none()

        # Return None if result is equal to it
        if not result:
            return None

        # Return first row of the result
        result = result[0].to_read_model()
        return result

    async def delete_referral_code(
        self,
        **kwargs,
    ) -> None:
        await self.delete_one(**kwargs)
