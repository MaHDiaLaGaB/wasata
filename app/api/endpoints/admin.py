import logging
from fastapi import APIRouter, status, Depends, HTTPException, Security
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    OAuth2PasswordBearer,
    APIKeyQuery,
    APIKeyHeader,
)

from app.db.schemas import AdminCreate
from app.services.admin_bl import AdminBL
from app.exceptions import Forbidden
from app.core.config import config
from itsdangerous import URLSafeSerializer

logger = logging.getLogger(__name__)

route = APIRouter(tags=["secret"])

security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@route.post("/admin", include_in_schema=True, status_code=status.HTTP_201_CREATED)
def admin_endpoint(*, api_key: str, admin: AdminCreate, admin_bl: AdminBL = Depends()):
    if config.SECRETS_ENCRYPTION_KEY != api_key:
        raise Forbidden

    admin.value = api_key
    logger.info("Craeting admin ... ")
    return admin_bl.create_admin(admin)
