from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from storage.db import async_session_maker
from respositories import (
    UserRepository,
    UserRepositoryBase,
    TokenBlacklistRepositoryBase,
    TokenBlacklistRepository,
    ReferralCodeRepository,
    ReferralCodeRepositoryBase,
    ReferralRepositoryBase,
    ReferralRepository,
)


class IUnitOfWork(ABC):
    user: UserRepositoryBase
    referral_code: ReferralCodeRepositoryBase
    token_blacklist: TokenBlacklistRepositoryBase
    referral: ReferralRepositoryBase

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.user = UserRepository(session=self.session)

        self.token_blacklist = TokenBlacklistRepository(session=self.session)

        self.referral_code = ReferralCodeRepository(session=self.session)

        self.referral = ReferralRepository(session=self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
