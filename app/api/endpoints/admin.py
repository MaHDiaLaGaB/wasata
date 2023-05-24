import logging
from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.db.schemas import AdminCreate
from app.services.admin_bl import AdminBL
from app.exceptions import Forbidden

logger = logging.getLogger(__name__)

route = APIRouter(tags=["secret"])

security = HTTPBasic()


def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "secret"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise Forbidden(description="You are not the admin")
    return credentials.username


@route.get("/admin", include_in_schema=True, status_code=status.HTTP_201_CREATED)
def admin_endpoint(*, admin: AdminCreate, admin_bl: AdminBL):
    logger.info("Craeting admin ... ")
    return admin_bl.create_admin(admin)
