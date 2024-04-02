"""
 Add an admin endpoints TODO i need to secure the endpoint with api secrets
"""
import logging

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from http import HTTPStatus
from app.db.sessions import AdminRepository
from app.db.schemas import AdminCreate, AdminUpdate
from app.db.database_engine import UserDB

from app.services.admin_bl import AdminBL
from app.exceptions import Forbidden
from app.core.config import config
from .routes import ADMIN, UPDATE_USDT

security = HTTPBasic()

logger = logging.getLogger(__name__)

route = APIRouter(tags=["admin"])


@route.post(ADMIN, include_in_schema=True, status_code=HTTPStatus.CREATED)
def admin_endpoint(
    *, secret_key: str, admin_create: AdminCreate, admin_bl: AdminBL = Depends()
):
    if config.SECRETS_ENCRYPTION_KEY != secret_key:
        raise Forbidden(description="Tik Tok.. Try Again")

    logger.info("Craeting admin ... ")
    logging.debug(f"Received request JSON: {admin_create}")
    return admin_bl.create_admin(admin_create=admin_create)


@route.put(UPDATE_USDT, include_in_schema=True, status_code=HTTPStatus.OK)
def update_usdt_price(
    *,
    admin_update: AdminUpdate,
    secret_key: str,
    admin_bl: AdminBL = Depends(),
) -> float:
    updated_price = admin_bl.update_price_admin(
        secret_key=secret_key, admin_update=admin_update
    )
    return updated_price.usdt_price
