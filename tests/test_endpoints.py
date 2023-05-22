from app.api.endpoints import routes
from fastapi import status


USER_1 = {"name": "mahdi", "email": "mahdi@example.com", "tokens": 300}


def test_health(test_app):
    resp = test_app.get(
        url=routes.HEALTH,
    )
    assert resp.status_code == status.HTTP_200_OK


def test_add_user(test_app):
    resp = test_app.post(url=routes.BUY, json=USER_1)
    assert resp.status_code == status.HTTP_201_CREATED
