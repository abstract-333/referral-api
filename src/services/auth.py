from datetime import datetime, timedelta
from typing import Mapping

import jwt
from argon2 import PasswordHasher
from fastapi import Depends
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jwt import ExpiredSignatureError
from pydantic import EmailStr, ValidationError

from common import IUnitOfWork
from exceptions import (
    ExceptionNotAcceptable406,
    ExceptionNotFound404,
    ExceptionForbidden403,
    ExceptionUnauthorized401,
)
from exceptions.error_code import ErrorCode
from schemas import (
    UserRead,
    AccessRefreshTokens,
    UserCreate,
    UserHashedPassword,
    UserInDB,
    TokenBlacklistInDB,
    TokenBlacklistCreate,
)
from settings import settings_obj

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/sign-in",
)


class AuthService:
    def __init__(
        self,
        is_superuser: bool = None,
        is_verified: bool = None,
        is_active: bool = None,
    ):
        self.is_verified = is_verified
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.password_hasher = PasswordHasher(
            hash_len=16, salt_len=16, memory_cost=65536 // 2
        )

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
    ) -> UserRead:
        current_user: UserRead = await self.validate_access_token(bytes(token, "utf-8"))
        await self.check_user_state(current_user=current_user)
        return current_user

    @classmethod
    async def _get_user(
        cls,
        uow: IUnitOfWork,
        **kwargs,
    ) -> UserInDB | None:
        """Get user by **kwargs"""
        async with uow:
            user: UserInDB | None = await uow.user.get_user(**kwargs)
            return user

    @classmethod
    async def add_user(
        cls,
        uow: IUnitOfWork,
        user_data: dict,
    ) -> None:
        """Add user to db"""
        async with uow:
            await uow.user.add_user(user_data)
            await uow.commit()

    @classmethod
    async def add_token_to_blacklist(cls, token_data: dict, uow: IUnitOfWork) -> None:
        async with uow:
            await uow.token_blacklist.add_token_to_blacklist(token_data)
            await uow.commit()

    @classmethod
    async def get_token_from_blacklist(
        cls,
        uow: IUnitOfWork,
        **kwargs,
    ) -> tuple[TokenBlacklistInDB] | None:
        async with uow:
            return await uow.token_blacklist.get_token_from_blacklist(**kwargs)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hasher.verify(
            password=plain_password, hash=hashed_password
        )

    async def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)

    @classmethod
    async def decode_token(cls, token: bytes) -> Mapping:
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings_obj.JWT_SECRET_KEY,
                algorithms=[settings_obj.JWT_ALGORITHM],
            )
            return payload

        except ExpiredSignatureError:
            raise ExceptionUnauthorized401(detail=ErrorCode.EXPIRED_TOKEN)

        except Exception:
            raise ExceptionUnauthorized401(detail=ErrorCode.JWT_TOKEN_INVALID)

    @classmethod
    async def extract_user_from_payload(
        cls,
        payload: Mapping,
    ) -> UserRead:
        exception = ExceptionUnauthorized401(
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
        user_data = payload.get("user")
        try:
            user = UserRead(**user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    async def extract_id_from_payload(cls, payload: Mapping) -> str:
        return payload.get("sub")

    @classmethod
    async def create_jwt_access_token(cls, user: UserRead) -> bytes:
        now = datetime.utcnow()
        payload: dict = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings_obj.JWT_EXPIRATION_ACCESS_TOKEN),
            "sub": str(user.id),
            "user": user.model_dump(mode="json"),
        }
        jwt_token: bytes = jwt.encode(
            payload=payload,
            key=settings_obj.JWT_SECRET_KEY,
            algorithm=settings_obj.JWT_ALGORITHM,
        )

        return jwt_token

    async def validate_access_token(self, token: bytes) -> UserRead:
        payload: Mapping = await self.decode_token(token=token)
        user: UserRead = await self.extract_user_from_payload(payload)

        return user

    @classmethod
    async def create_jwt_refresh_token(cls, user_id: str) -> bytes:
        now = datetime.utcnow()
        payload: dict = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings_obj.JWT_EXPIRATION_REFRESH_TOKEN),
            "sub": user_id,
        }
        jwt_token: bytes = jwt.encode(
            payload=payload,
            key=settings_obj.JWT_SECRET_KEY,
            algorithm=settings_obj.JWT_ALGORITHM,
        )

        return jwt_token

    async def register_new_user(
        self,
        user_data: UserCreate,
        uow: IUnitOfWork,
    ) -> bool:
        exception_email = ExceptionNotAcceptable406(
            detail=ErrorCode.EMAIL_ALREADY_EXISTS
        )

        # Check that email is not already taken
        user_with_same_email: UserInDB | None = await self._get_user(
            email=user_data.email, uow=uow
        )
        if user_with_same_email is not None:
            raise exception_email

        hashed_password: str = await self.hash_password(user_data.password)
        user = UserHashedPassword(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )
        await self.add_user(
            user_data=user.model_dump(
                exclude={"is_active", "is_verified", "is_superuser"}
            ),
            uow=uow,
        )

        return True

    async def get_user_by_email(self, email: EmailStr, uow: IUnitOfWork) -> UserRead:
        try:
            returend_user: UserRead | None = await self._get_user(email=email, uow=uow)

            if not returend_user:
                raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

            return returend_user

        except Exception as e:
            raise e

    async def authenticate_user(
        self,
        email: str,
        password: str,
        uow: IUnitOfWork,
    ) -> AccessRefreshTokens:
        exception = ExceptionNotFound404(detail=ErrorCode.LOGIN_BAD_CREDENTIALS)
        user: UserInDB | None = await self._get_user(email=email, uow=uow)

        if not user:
            raise exception

        try:
            await self.verify_password(
                plain_password=password,
                hashed_password=user.hashed_password,
            )
        except Exception:
            raise exception

        await self.check_user_state(current_user=user)
        return await self.generate_access_refresh_tokens_from_user(user=user)

    async def generate_access_refresh_tokens_from_user(
        self, user: UserRead
    ) -> AccessRefreshTokens:
        access_token: bytes = await self.create_jwt_access_token(user=user)
        refresh_token: bytes = await self.create_jwt_refresh_token(
            user_id=str(object=user.id),
        )
        return AccessRefreshTokens(
            access_token=access_token, refresh_token=refresh_token
        )

    async def check_user_state(
        self,
        current_user: UserRead,
    ):
        if self.is_verified and current_user.is_verified != self.is_verified:
            raise ExceptionForbidden403(detail=ErrorCode.USER_NOT_VERIFIED)

        if self.is_active and current_user.is_active != self.is_active:
            raise ExceptionForbidden403(detail=ErrorCode.USER_INACTIVE)

        if self.is_superuser and current_user.is_superuser != self.is_superuser:
            raise ExceptionForbidden403(detail=ErrorCode.USER_NOT_ADMIN)

    async def validate_refresh_token(
        self,
        uow: IUnitOfWork,
        refresh_token: bytes,
    ) -> UserRead:
        payload: Mapping = await self.decode_token(refresh_token)

        user_argument: dict = payload.get("user")
        if user_argument is not None:
            raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_REFRESH_TOKEN)

        user_id: str = await self.extract_id_from_payload(payload)
        current_user: UserRead | None = await self._get_user(id=user_id, uow=uow)

        if current_user is None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        blocked_refresh_tokens: tuple[TokenBlacklistInDB] | None = (
            await self.get_token_from_blacklist(
                token=str(object=refresh_token, encoding="utf-8"),
                user_id=current_user.id,
                uow=uow,
            )
        )
        if blocked_refresh_tokens:
            raise ExceptionForbidden403(detail=ErrorCode.BLOCKED_REFRESH_TOKEN)

        return current_user

    async def create_tokens(
        self,
        uow: IUnitOfWork,
        refresh_token: bytes,
    ) -> AccessRefreshTokens:
        current_user: UserRead = await self.validate_refresh_token(
            refresh_token=refresh_token, uow=uow
        )
        await self.check_user_state(current_user=current_user)
        revoked_token = TokenBlacklistCreate(
            user_id=current_user.id, token=str(refresh_token, "utf-8")
        )
        await self.add_token_to_blacklist(revoked_token.model_dump(), uow=uow)
        return await self.generate_access_refresh_tokens_from_user(user=current_user)

    async def revoke_token(
        self,
        uow: IUnitOfWork,
        refresh_token: bytes,
    ) -> None:
        current_user: UserRead = await self.validate_refresh_token(
            refresh_token=refresh_token, uow=uow
        )
        await self.check_user_state(current_user=current_user)
        revoked_token = TokenBlacklistCreate(
            user_id=current_user.id, token=str(object=refresh_token, encoding="utf-8")
        )
        await self.add_token_to_blacklist(
            token_data=revoked_token.model_dump(), uow=uow
        )
