from .base import SQLAlchemyRepository, AbstractSQLRepository
from .faculty import FacultyRepository, FacultyRepositoryBase
from .lecturer import LecturerRepository, LecturerRepositoryBase
from .speciality import SpecialityRepository, SpecialityRepositoryBase
from .student import StudentRepository, StudentRepositoryBase
from .token_blacklist import TokenBlacklistRepositoryBase, TokenBlacklistRepository
from .user import UserRepository, UserRepositoryBase
