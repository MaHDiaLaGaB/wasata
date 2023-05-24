import logging
from fastapi import APIRouter, status, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, APIKeyQuery, APIKeyHeader

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


# def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = "admin"
#     correct_password = "secret"
#     if credentials.username != correct_username or credentials.password != correct_password:
#         raise Forbidden(description="You are not the admin")
#     return credentials.username


# async def get_current_admin(token: str = Depends(oauth2_scheme)):
#     # Verify token and get admin details
#     if config.SECRETS_ENCRYPTION_KEY != token:
#         raise Forbidden
#     if not admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return admin


# async def get_api_key(
#         api_key: str,
#         api_keyQuery: str = Security(api_key_query),
#         api_keyHeader: str = Security(api_key_header)
# ):
#     if api_keyQuery == api_key:
#         return api_keyQuery
#     elif api_keyHeader == api_key:
#         return api_keyHeader
#     else:
#         raise HTTPException(status_code=401, detail="Invalid API key")


@route.post("/admin", include_in_schema=True, status_code=status.HTTP_201_CREATED)
def admin_endpoint(*, api_key: str, admin: AdminCreate, admin_bl: AdminBL = Depends()):
    if config.SECRETS_ENCRYPTION_KEY != api_key:
        raise Forbidden

    admin.value = api_key
    logger.info("Craeting admin ... ")
    return admin_bl.create_admin(admin)
