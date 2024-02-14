from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from common import IUnitOfWork, UnitOfWork
from schemas import UserRead
from services import AuthService
from storage.db import get_async_session

get_current_active_user = AuthService(is_active=True).get_current_user
get_current_verified_user = AuthService(
    is_verified=True, is_active=True
).get_current_user
get_current_superuser = AuthService(is_superuser=True, is_active=True).get_current_user
UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CurrentActiveUserDep = Annotated[UserRead, Depends(get_current_active_user)]
CurrentVerifiedUserDep = Annotated[UserRead, Depends(get_current_verified_user)]
CurrentSuperUserDep = Annotated[UserRead, Depends(get_current_superuser)]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]
