import uuid
from abc import ABC, abstractmethod
from typing import Tuple

from sqlalchemy import Select, select

from models import UsersOrm
from models.referral import ReferralsOrm
from respositories import SQLAlchemyRepository, AbstractSQLRepository
from schemas import UserInDB


class UserRepositoryBase(AbstractSQLRepository[UserInDB], ABC):
    @abstractmethod
    async def get_user(self, **kwargs) -> UserInDB | None: ...

    @abstractmethod
    async def add_user(self, user_data: dict) -> None: ...

    @abstractmethod
    async def edit_user(self, user_data: dict, **kwargs) -> None: ...

    @abstractmethod
    async def join_users_by_referral_id(
        self,
        referrer_id: uuid.UUID,
    ) -> Tuple[UsersOrm] | None: ...


class UserRepository(SQLAlchemyRepository[UserInDB], UserRepositoryBase):
    model_cls = UsersOrm

    async def get_user(self, **kwargs) -> UserInDB | None:
        """Get user from db by **kwargs"""
        user: UserInDB | None = await self.find_one(**kwargs)
        return user

    async def join_users_by_referral_id(
        self,
        referrer_id: uuid.UUID,
    ) -> Tuple[UserInDB] | None:
        query: Select[Tuple[UsersOrm]] = (
            select(UsersOrm)
            .join(ReferralsOrm, UsersOrm.id == ReferralsOrm.referral_id)
            .filter(ReferralsOrm.referrer_id == referrer_id)
        )
        result = await self.session.execute(query)
        result = tuple(row[0].to_read_model() for row in result.all())

        if not result:
            return None

        return result

    async def add_user(self, user_data: dict) -> None:
        """Add user to db"""
        await self.add_one(user_data)

    async def edit_user(self, user_data: dict, **kwargs) -> None:
        """Edit user by **kwargs"""
        await self.edit_one(user_data, **kwargs)
