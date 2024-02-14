import os
from typing import Final

from pydantic_settings import BaseSettings

MINUTE: Final[int] = 60
HOUR: Final[int] = MINUTE * 60
DAY: Final[int] = HOUR * 24
MONTH: Final[int] = DAY * 30

# To make alembic finds path correctly
additional_path: str = ""
if os.path.exists("src/"):
    additional_path = "src/"


class Settings(BaseSettings):
    """There fields are rewritten by .env file"""

    # JWT
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_ACCESS_TOKEN: int = HOUR
    JWT_EXPIRATION_REFRESH_TOKEN: int = MONTH

    # Server
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    # DB
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Nado id
    NANO_ID_LENGTH: int = 10
    REFERRAL_CODE_EXPIRATION: int = DAY

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Hunter.com serivce that checks whether email is valid
    EMAIL_VERIFIER_API_KEY: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"

    class Config:
        """If .env.local exists it will load it.
        Otherwise load .env.prod"""

        env_file: str = (
            f"{additional_path}.env.local"
            if os.path.exists(path=f"{additional_path}.env.local")
            else f"{additional_path}.env.prod"
        )
        env_file_encoding = "utf-8"


settings_obj: Settings = Settings()
