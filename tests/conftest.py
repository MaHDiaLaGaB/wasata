import pytest
from sqlalchemy.orm import Session
from typing import Generator, Any
from starlette.testclient import TestClient
from app.server import app

from app.api.dependencies import BinanceWa
from app.db.database_engine import UserDB
from app.db.sessions import UserRepository, AdminRepository
from app.services.user_bl import UserBL
from app.services.admin_bl import AdminBL


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


user_db = UserDB()


@pytest.fixture(autouse=True)
def run_around_tests() -> Generator[Any, Any, Any]:
    user_db.reset()
    yield
    user_db.reset()


@pytest.fixture(autouse=True)
def user_db_session() -> Session:
    with user_db.create_session(commit_on_flush=True):
        yield user_db.session


@pytest.fixture()
def user_repository() -> UserRepository:
    return UserRepository(user_db)


@pytest.fixture()
def admin_repository() -> AdminRepository:
    return AdminRepository(user_db)


@pytest.fixture()
def user_bl(user_repository: UserRepository) -> UserBL:
    return UserBL(user_repository)


@pytest.fixture()
def admin_bl(admin_repository: AdminRepository) -> AdminBL:
    return AdminBL(admin_repository)


# this for spot3
@pytest.fixture()
def spot3_binance_api():
    binance_class = BinanceWa()
    yield binance_class
