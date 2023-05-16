from app.api.endpoints import routes
from fastapi import status


def test_health(test_client):
    resp = test_client.get(
        url=routes.HEALTH,
    )
    assert resp.status_code == status.HTTP_200_OK
