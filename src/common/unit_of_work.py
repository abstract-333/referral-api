from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from models import async_session_maker
from respository import (
    UserRepository,
    StudentRepository,
    FacultyRepository,
    LecturerRepository,
    SpecialityRepository,
    FacultyRepositoryBase,
    UserRepositoryBase,
    SpecialityRepositoryBase,
    StudentRepositoryBase,
    LecturerRepositoryBase,
    TokenBlacklistRepositoryBase,
    TokenBlacklistRepository,
)


class IUnitOfWork(ABC):
    user: UserRepositoryBase
    student: StudentRepositoryBase
    faculty: FacultyRepositoryBase
    lecturer: LecturerRepositoryBase
    speciality: SpecialityRepositoryBase
    token_blacklist: TokenBlacklistRepositoryBase

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.user = UserRepository(self.session)
        self.student = StudentRepository(self.session)
        self.faculty = FacultyRepository(self.session)
        self.lecturer = LecturerRepository(self.session)
        self.speciality = SpecialityRepository(self.session)
        self.token_blacklist = TokenBlacklistRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
