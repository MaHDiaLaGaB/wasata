"""
 Add an admin endpoints TODO i need to secure the endpoint with api secrets
"""
import logging

from fastapi import APIRouter, status, Depends

from app.db.schemas import AdminCreate
from app.services.admin_bl import AdminBL
from app.exceptions import Forbidden
from app.core.config import config
from .routes import ADMIN

logger = logging.getLogger(__name__)

route = APIRouter(tags=["admin"])


@route.post(ADMIN, include_in_schema=True, status_code=status.HTTP_201_CREATED)
def admin_endpoint(
    *, api_key: str, admin_create: AdminCreate, admin_bl: AdminBL = Depends()
):
    if config.SECRETS_ENCRYPTION_KEY != api_key:
        raise Forbidden(description="FUCK OFF.. YOU ARE NOT THE ADMIN")

    logger.info("Craeting admin ... ")
    return admin_bl.create_admin(admin_data=admin_create)
