from abc import ABC, abstractmethod

from models import TokensBlacklistOrm
from respositories import SQLAlchemyRepository, AbstractSQLRepository
from schemas import TokenBlacklistInDB


class TokenBlacklistRepositoryBase(AbstractSQLRepository[TokenBlacklistInDB], ABC):
    @abstractmethod
    async def add_token_to_blacklist(self, token_data: dict) -> None: ...

    @abstractmethod
    async def get_token_from_blacklist(
        self, **kwargs
    ) -> tuple[TokenBlacklistInDB] | None: ...


class TokenBlacklistRepository(
    SQLAlchemyRepository[TokenBlacklistInDB], TokenBlacklistRepositoryBase
):
    model_cls = TokensBlacklistOrm

    async def add_token_to_blacklist(self, token_data: dict) -> None:
        await self.add_one(data=token_data)

    async def get_token_from_blacklist(
        self, **kwargs
    ) -> tuple[TokenBlacklistInDB] | None:
        tokens: tuple[TokenBlacklistInDB] | None = await self.find_by(**kwargs)
        return tokens
