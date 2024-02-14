from typing import Final

from pydantic_settings import BaseSettings

MINUTE: Final[int] = 60
HOUR: Final[int] = MINUTE * 60
DAY: Final[int] = HOUR * 24
MONTH: Final[int] = DAY * 30


class Settings(BaseSettings):
    """There fields are rewritten by env file"""

    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_ACCESS_TOKEN: int = HOUR
    JWT_EXPIRATION_REFRESH_TOKEN: int = MONTH
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SENTRY_URL: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    TELEGRAM_API_KEY: str = ""
    TELEGRAM_CHANNEL_ID: int = -1
    TELEGRAM_API_ID: int = 0
    TELEGRAM_HASH: str = ""

    @property
    def database_url(self):
        # return "postgresql+asyncpg://final_project_qirm_user:UbMyPUOTEVwD4uTR8gFXa8kd7cPpZBYw@dpg-clcac1t4lnec73e1kasg-a.frankfurt-postgres.render.com/final_project_qirm?async_fallback=True"
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings_obj: Settings = Settings()
