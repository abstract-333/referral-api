from fastapi import APIRouter
from starlette import status

from dependencies import UOWDep, OAuth2Dep
from schemas import AccessRefreshTokens
from services import AuthService
from .docs import sign_in_response, sign_out_response, get_tokens_response

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post(
    path="/sign-in",
    response_model=AccessRefreshTokens,
    responses=sign_in_response,
)
async def sign_in(
    uow: UOWDep,
    form_data: OAuth2Dep,
) -> AccessRefreshTokens:
    auth_service = AuthService(is_active=True)
    return await auth_service.authenticate_user(
        email=form_data.username, password=form_data.password, uow=uow
    )


@auth_router.post(
    path="/get-tokens",
    response_model=AccessRefreshTokens,
    status_code=status.HTTP_200_OK,
    responses=get_tokens_response,
)
async def get_access_refresh_tokens(
    uow: UOWDep,
    refresh_token: str,
) -> AccessRefreshTokens:
    auth_service = AuthService(is_active=True)
    refresh_token_string: bytes = bytes(refresh_token, "utf-8")
    return await auth_service.create_tokens(refresh_token=refresh_token_string, uow=uow)


@auth_router.post(
    path="/sign-out",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=sign_out_response,
)
async def sign_out(
    uow: UOWDep,
    refresh_token: str,
) -> None:
    auth_service = AuthService(is_active=True)
    refresh_token_string: bytes = bytes(refresh_token, "utf-8")
    await auth_service.revoke_token(refresh_token=refresh_token_string, uow=uow)
