import logging
from fastapi import APIRouter, status, Depends

from .routes import BUY
from app.db.schemas import UserCreate, UserGet
from http import HTTPStatus
from app.db.database_engine import UserDB
from app.db.models import Users
from app.services.user_bl import UserBL
from app.exceptions import Forbidden


logger = logging.getLogger(__name__)

route = APIRouter(tags=["users"])

user_db = UserDB()


@route.post(
    BUY,
    status_code=HTTPStatus.CREATED,
)
def create(
    *,
    user: UserCreate,
    # key: str,
    user_bl: UserBL = Depends(),
):
    """
    create a user, only for tests
    - *access:* secret key
    - **body**: a UserCreate object
    """
    # if key != config.AUTH0_CALLBACK_KEY:
    #     raise Forbidden()
    logging.info(f"Adding new user {user}")
    if user.tokens <= 0:
        raise ValueError("Price must be greater than 0")

    return user_bl.create_user(user)
