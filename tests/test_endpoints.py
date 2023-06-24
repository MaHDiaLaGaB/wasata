from app.api.endpoints import routes
from http import HTTPStatus
import logging
from fastapi.testclient import TestClient
from app.core.config import config
from app.db.sessions import AdminRepository, UserRepository
from app.services.payments import PaymentGetaway

USER_1 = {
    "tokens": 9,
    "phone_number": "0923003030",
}

params = {"wallet_address": "wallet_address", "admin_username": "admin"}

ADMIN_1 = {"username": "admin", "password": "password", "usdt_price": 5.5}


def test_health(client: TestClient):
    resp = client.get(
        url=routes.HEALTH,
    )
    assert resp.status_code == HTTPStatus.OK


def test_add_user(
    client: TestClient,
    admin_repository: AdminRepository,
    user_repository: UserRepository,
):
    res = client.post(
        routes.ADMIN, json=ADMIN_1, params={"secret_key": config.SECRETS_ENCRYPTION_KEY}
    )
    assert res.status_code == HTTPStatus.CREATED

    admin = admin_repository.get(ADMIN_1["username"])

    assert admin.usdt_price == 5.5

    resp = client.post(url=routes.BUY, json=USER_1, params=params)
    logging.info(f"{resp.json()}")
    assert resp.status_code == HTTPStatus.CREATED


def test_add_admin(client: TestClient, admin_repository: AdminRepository):
    response = client.post(
        routes.ADMIN, json=ADMIN_1, params={"secret_key": config.SECRETS_ENCRYPTION_KEY}
    )

    assert response.status_code == HTTPStatus.CREATED
