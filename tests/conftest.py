import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
import requests
from app.server import app
from app.core.config import config
from app.api.dependencies import BinanceWa


DATABASE_URL = "postgresql://user:password@localhost/test_db"


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture
def spot_binance_api():
    api_key = config.TEST_BIBANCE_API_KEY
    api_secret = config.TEST_BINANCE_SECRET_API
    base_url = config.TEST_BINANCE_URL
    binance_class = BinanceWa(
        binance_api_key=api_key, binance_api_secret=api_secret, base_url=base_url
    )
    yield binance_class


# this for spot3
@pytest.fixture
def spot3_binance_api():
    api_key = config.BINANCE_API_KEY
    api_secret = config.BINANCE_SECRETE_KEY
    base_url = config.BINANCE_BASE_URL
    binance_class = BinanceWa(
        binance_api_key=api_key, binance_api_secret=api_secret, base_url=base_url
    )
    yield binance_class


# @pytest.fixture(scope="module")
# def test_db():
#     engine = create_engine(DATABASE_URL)
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     BaseModel.metadata.create_all(bind=engine)
#
#     def override_get_db():
#         db = TestingSessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()
#
#     app.dependency_overrides[get_engine()] = override_get_db
#
#     yield engine
#
#     BaseModel.metadata.drop_all(bind=engine)
#
#
# @pytest.fixture(scope="function")
# async def test_async_db():
#     async_db = Database(DATABASE_URL)
#     await async_db.connect()
#
#     yield async_db
#
#     await async_db.disconnect()
