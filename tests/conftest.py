from fastapi.testclient import TestClient
from app.server import app
import pytest


@pytest.fixture()
def test_client():
    client = TestClient(app=app)
    yield client
