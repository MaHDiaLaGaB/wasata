# type: ignore
from dotenv import load_dotenv
from .base_configuration import BaseConfig
from app.core import generate_config
from typing import cast
import os

load_dotenv()


class Config(BaseConfig):
    NAME = "FastAPI"
    VERSION = "V1"
    ENV = os.environ.get("ENV", "test")
    WASATA_PORT = 8080
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password"

    # postgres
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = 5432
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
    DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DB_CONNECTION_TIMEOUT = 5

    # secret to change anything here
    SECRETS_ENCRYPTION_KEY = os.environ.get("SECRETS_ENCRYPTION_KEY")

    # Binance
    BINANCE_SECRETE_KEY = os.environ.get("BINANCE_SECRETE_KEY")
    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
    BINANCE_BASE_URL = "https://api.binance.com"
    COIN = "USDT"
    BSCAN_API_KEY = os.environ.get("BSCAN_API_KEY")

    # mo3amalat
    MO3AMALAT_HOST = os.environ.get("MOAMALAT_HOST", "localhost")
    MO3AMALAT_CHECKOUT = os.environ.get("MOAMALAT_CHECKOUT")
    MOAMALAT_TRANSACTIONS_APPROVED = os.environ.get("MOAMALAT_TRANSACTIONS_APPROVED")


config = cast(Config, generate_config(Config))  # pylint: disable=C0103
config.WASATA_PORT = int(config.WASATA_PORT)
config.ENV = config.ENV
config.ADMIN_USERNAME = config.ADMIN_USERNAME
config.ADMIN_PASSWORD = config.ADMIN_PASSWORD
config.POSTGRES_USER = config.POSTGRES_USER
config.POSTGRES_PASSWORD = config.POSTGRES_PASSWORD
config.POSTGRES_PORT = int(config.POSTGRES_PORT)
config.POSTGRES_DB = config.POSTGRES_DB
config.DB_CONNECTION_TIMEOUT = int(config.DB_CONNECTION_TIMEOUT)
config.DATABASE_URI = config.DATABASE_URI
config.SECRETS_ENCRYPTION_KEY = config.SECRETS_ENCRYPTION_KEY
config.BINANCE_SECRETE_KEY = config.BINANCE_SECRETE_KEY
config.BINANCE_BASE_URL = config.BINANCE_BASE_URL
config.BINANCE_API_KEY = config.BINANCE_API_KEY
config.BSCAN_API_KEY = config.BSCAN_API_KEY
config.MO3AMALAT_HOST = config.MO3AMALAT_HOST
config.MO3AMALAT_CHECKOUT = config.MO3AMALAT_CHECKOUT
config.MOAMALAT_TRANSACTIONS_APPROVED = config.MOAMALAT_TRANSACTIONS_APPROVED

config = Config()
