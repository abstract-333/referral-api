from abc import abstractmethod, ABC
from types import NoneType
from typing import TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import BaseModelORM

T = TypeVar("T", bound=BaseModel)


class AbstractSQLRepository(Generic[T], ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> None: ...

    @abstractmethod
    async def edit_one(self, data: dict, **kwargs) -> None: ...

    @abstractmethod
    async def find_by(
        self, offset: int = None, limit: int = None, **kwargs
    ) -> tuple[T] | None: ...

    @abstractmethod
    async def find_one(self, **kwargs) -> T | None: ...

    @abstractmethod
    async def delete_one(self, **kwargs) -> None: ...


class SQLAlchemyRepository(AbstractSQLRepository[T], ABC):
    model_cls: type[BaseModelORM] = NoneType

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict) -> None:
        stmt = insert(self.model_cls).values(**data)
        await self.session.execute(stmt)

    async def edit_one(self, data: dict, **kwargs) -> None:
        stmt = update(self.model_cls).filter_by(**kwargs).values(**data)
        await self.session.execute(stmt)

    async def find_by(
        self, offset: int = None, limit: int = None, **kwargs
    ) -> tuple[T] | None:
        query = select(self.model_cls).filter_by(**kwargs).offset(offset).limit(limit)
        result = await self.session.execute(query)
        result = tuple(row[0].to_read_model() for row in result.all())

        if not result:
            return None

        return result

    async def find_one(self, **kwargs) -> T | None:
        query = select(self.model_cls).filter_by(**kwargs)
        result = await self.session.execute(query)
        result = result.one_or_none()

        # Return None if result is equal to it
        if not result:
            return None

        # Return first row of the result
        result = result[0].to_read_model()
        return result

    async def delete_one(self, **kwargs) -> None:
        stmt = delete(self.model_cls).filter_by(**kwargs)
        await self.session.execute(stmt)
