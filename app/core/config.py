import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Config(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str | None = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str | None = os.getenv("POSTGRES_PORT")
    POSTGRES_NAME: str | None = os.getenv("POSTGRES_DB")
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

    SECRETS_ENCRYPTION_KEY: str = os.getenv("SECRETS_ENCRYPTION_KEY", "my_secrete_key")
    MY_ADMIN_PASSWORD = os.getenv("MY_ADMIN_PASSWORD")

    DB_CONNECTION_TIMEOUT: int = 5

    # Binance
    BINANCE_SECRETE_KEY = os.getenv("BINANCE_SECRETE_KEY")
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")
    COIN = "USDT"
    PRICE: float | None = os.getenv("PRICE")

    # test binance
    TEST_BINANCE_URL = os.getenv("TEST_BINANCE_URL")
    TEST_BIBANCE_API_KEY = os.getenv("TEST_BIBANCE_API_KEY")
    TEST_BINANCE_SECRET_API = os.getenv("TEST_BINANCE_SECRET_API")

    class Config:
        env_file = ".env"


config = Config()
