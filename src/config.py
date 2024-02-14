import os

from dotenv import load_dotenv


# If .env.local exists it will load it.
if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    # Otherwise load .env.prod
    load_dotenv(".env.prod")

DB_HOST: str | None = os.environ.get("DB_HOST")
DB_USER: str | None = os.environ.get("DB_USER")
DB_PASSWORD: str | None = os.environ.get("DB_PASSWORD")
DB_PORT: str | None = os.environ.get("DB_PORT")
DB_NAME: str | None = os.environ.get("DB_NAME")

AUTH_JWT_KEY: str | None = os.environ.get("JWT_SECRET_KEY")

NANO_ID_LENGTH: str | None = os.environ.get("NANO_ID_LENGTH")

REDIS_HOST: str | None = os.environ.get("REDIS_HOST")
REDIS_PORT: str | None = os.environ.get("REDIS_PORT")

EMAIL_VERIFIER_API_KEY: str | None = os.environ.get("EMAIL_VERIFIER_API_KEY")
