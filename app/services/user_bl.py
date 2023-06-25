import logging

from fastapi import Depends
from app.core.config import config
from app.db.models import Users

from app.db.schemas import UserCreate, UserUpdate
from app.db.sessions import UserRepository

logger = logging.getLogger(__name__)


class UserBL:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository

    # for now, we are creating invoices for each user creation
    def create_user(self, user_create: UserCreate) -> Users:
        # user = self.user_repository.get_by_number(user_create.phone_number)
        # if user is None:
        return self.user_repository.create(user_create)
