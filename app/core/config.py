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
    ENV = os.environ.get("ENVIRONMENT", "test")
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

    # mailjet
    MJ_APIKEY_PUBLIC = os.environ.get("MJ_APIKEY_PUBLIC")
    MJ_APIKEY_PRIVATE = os.environ.get("MJ_APIKEY_PRIVATE")

    # secret to change anything here
    SECRETS_ENCRYPTION_KEY = os.environ.get("SECRETS_ENCRYPTION_KEY")

    # Binance
    BINANCE_SECRETE_KEY = os.environ.get("BINANCE_SECRETE_KEY")
    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
    BINANCE_BASE_URL = "https://api.binance.com"
    COIN = "USDT"
    BSCAN_API_KEY = os.environ.get("BSCAN_API_KEY")

    #Tlync
    TLYNC_TEST_BASE_URL = os.environ.get("TLYNC_TEST_BASE_URL")
    TLYNC_BASE_URL = os.environ.get("TLYNC_BASE_URL")
    TLYNC_TOKEN = os.environ.get("TLYNC_TOKEN")
    TLYNC_STORE_ID = os.environ.get("TLYNC_STORE_ID")


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
config.MJ_APIKEY_PUBLIC = config.MJ_APIKEY_PUBLIC
config.MJ_APIKEY_PRIVATE = config.MJ_APIKEY_PRIVATE
config.TLYNC_BASE_URL = config.TLYNC_BASE_URL
config.TLYNC_TOKEN = config.TLYNC_TOKEN
config.TLYNC_STORE_ID = config.TLYNC_STORE_ID
config.TLYNC_TEST_BASE_URL = config.TLYNC_TEST_BASE_URL

config = Config()
