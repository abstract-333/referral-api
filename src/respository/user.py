from abc import ABC, abstractmethod

from models import UsersOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas import UserReadWithPassword


class UserRepositoryBase(AbstractSQLRepository[UserReadWithPassword], ABC):
    @abstractmethod
    async def get_user(self, **kwargs) -> UserReadWithPassword | None:
        ...

    @abstractmethod
    async def add_user(self, user_data: dict) -> None:
        ...

    @abstractmethod
    async def edit_user(self, user_data: dict, **kwargs) -> None:
        ...


class UserRepository(SQLAlchemyRepository[UserReadWithPassword], UserRepositoryBase):
    model_cls = UsersOrm

    async def get_user(self, **kwargs) -> UserReadWithPassword | None:
        """Get user from db by **kwargs"""
        user: UserReadWithPassword | None = await self.find_one(**kwargs)
        return user

    async def add_user(self, user_data: dict) -> None:
        """Add user to db"""
        await self.add_one(user_data)

    async def edit_user(self, user_data: dict, **kwargs) -> None:
        """Edit user by **kwargs"""
        await self.edit_one(user_data, **kwargs)
