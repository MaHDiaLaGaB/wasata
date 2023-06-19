import os
from dotenv import load_dotenv
from .base_configuration import BaseConfig

load_dotenv()


class Config(BaseConfig):
    TITLE: str = os.getenv("TITLE", "FastAPI")
    VERSION: str = os.getenv("VERSION", "V1")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    WASATA_PORT: int = int(os.getenv("WASATA_PORT"))
    ADMIN_USERNAME: str = os.getenv("USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("PASSWORD", "password")

    # postgres
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str | None = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str | None = os.getenv("POSTGRES_PORT")
    POSTGRES_NAME: str | None = os.getenv("POSTGRES_DB")
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

    # dev sqlight3
    DATABASE_URI_DEV: str = os.getenv("DATABASE_URL_DEV")

    # secret to change anything here
    SECRETS_ENCRYPTION_KEY: str | None = os.getenv("SECRETS_ENCRYPTION_KEY")
    DB_CONNECTION_TIMEOUT: int = 5

    # Binance
    BINANCE_SECRETE_KEY = os.getenv("BINANCE_SECRETE_KEY")
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")
    COIN = os.getenv("COIN")
    PRICE: float | None = os.getenv("PRICE")

    # test binance
    TEST_BINANCE_URL = os.getenv("TEST_BINANCE_URL")
    TEST_BIBANCE_API_KEY = os.getenv("TEST_BIBANCE_API_KEY")
    TEST_BINANCE_SECRET_API = os.getenv("TEST_BINANCE_SECRET_API")

    # mo3amalat
    MO3AMALAT_CHECKOUT = os.getenv("MOAMALAT_CHECKOUT")
    MOAMALAT_TRANSACTIONS_APPROVED = os.getenv("MOAMALAT_TRANSACTIONS_APPROVED")

    class Config:
        env_file = ".env"


config = Config()
