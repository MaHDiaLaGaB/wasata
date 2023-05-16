import logging
from fastapi import APIRouter, status, HTTPException
from .routes import HEALTH

logger = logging.getLogger(__name__)

route = APIRouter(tags=["health"])


# ---------------------
# Health check endpoint
# ---------------------
@route.get(HEALTH, include_in_schema=True, status_code=status.HTTP_200_OK)
def health_check():
    try:
        return {"status": f"ok {status.HTTP_200_OK}"}
    except HTTPException as e:
        logger.error(f"can't reach the API because of: {e}")
        raise
