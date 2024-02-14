from pydantic import BaseModel, Field

from settings import settings_obj


class AccessRefreshTokens(BaseModel):
    access_token: bytes = Field(
        description=f"Valid for {int(settings_obj.JWT_EXPIRATION_ACCESS_TOKEN / 60)} minutes"
    )
    refresh_token: bytes = Field(
        description=f"Valid for {int(settings_obj.JWT_EXPIRATION_REFRESH_TOKEN / 3600 / 24 / 30)} months"
    )
    token_type: str = Field(
        default="bearer",
    )
