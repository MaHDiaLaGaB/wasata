import os
from dotenv import load_dotenv
from .base_configuration import BaseConfig
from typing import Any

load_dotenv()


class Config(BaseConfig):
    TITLE = os.getenv("TITLE", "FastAPI")
    VERSION = os.getenv("VERSION", "V1")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
    WASATA_PORT: int = os.getenv("WASATA_PORT", 8080)
    ADMIN_USERNAME = os.getenv("USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("PASSWORD", "password")

    # postgres
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_NAME = os.getenv("POSTGRES_DB", "postgres")
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

    # dev sqlight3
    DATABASE_URI_DEV = os.getenv("DATABASE_URL_DEV", "")

    # secret to change anything here
    SECRETS_ENCRYPTION_KEY = os.getenv("SECRETS_ENCRYPTION_KEY", "")
    DB_CONNECTION_TIMEOUT = 5

    # Binance
    BINANCE_SECRETE_KEY = os.getenv("BINANCE_SECRETE_KEY", "")
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL", "")
    COIN = os.getenv("COIN", "USDT")
    PRICE: float = os.getenv("PRICE")

    # test binance
    TEST_BINANCE_URL = os.getenv("TEST_BINANCE_URL", "")
    TEST_BIBANCE_API_KEY = os.getenv("TEST_BIBANCE_API_KEY", "")
    TEST_BINANCE_SECRET_API = os.getenv("TEST_BINANCE_SECRET_API", "")

    # mo3amalat
    MO3AMALAT_CHECKOUT = os.getenv("MOAMALAT_CHECKOUT", "")
    MOAMALAT_TRANSACTIONS_APPROVED = os.getenv("MOAMALAT_TRANSACTIONS_APPROVED", "")

    class Config:
        env_file = ".env"


config = Config()
