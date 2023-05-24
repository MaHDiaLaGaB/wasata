import os
from dotenv import load_dotenv
from pydantic import BaseSettings, condecimal

load_dotenv()


class Config(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_NAME: str = os.getenv("POSTGRES_DB")
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

    SECRETS_ENCRYPTION_KEY = os.getenv("SECRETS_ENCRYPTION_KEY")
    MY_ADMIN_PASSWORD = os.getenv("MY_ADMIN_PASSWORD")

    DB_CONNECTION_TIMEOUT: int = 5

    class Config:
        env_file = ".env"


config = Config()
