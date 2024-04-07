"""
Manages database connections and sessions.
"""
from typing import Any

from .models import Users, UsersBase, Admins

from .schemas import UserCreate, WasataBase, AdminCreate, UserUpdate, AdminUpdate
from fastapi import Depends
from sqlalchemy.types import Numeric
from cus_exceptions import ObjectNotFound
import logging
from .database_engine import UserDB, get_user_db
from typing import TypeVar, Type, cast, Union, Dict
from uuid import UUID
from sqlalchemy import func

# ----------------------
# User functions
# ----------------------

T = TypeVar("T", bound=UsersBase)  # type: ignore

logger = logging.getLogger(__name__)


class BaseRepository:
    """
    Base Database Repo
    """

    def __init__(
        self, db: UserDB = Depends(get_user_db)  # pylint: disable=C0103
    ) -> None:
        self.db = db  # pylint: disable=C0103

    def _create(self, entity: T) -> T:
        self.db.session.add(entity)
        self.db.flush()
        return entity

    def _get_by_id(self, model: Type[T], entity_id: UUID) -> T:
        entity = self.db.session.query(model).get(entity_id)
        if not entity:
            raise ObjectNotFound(str(entity_id))
        return cast(T, entity)

    def _get_one(self, model: Type[T], **kwargs: Union[str, UUID]) -> T:
        entity = self.db.session.query(model).filter_by(**kwargs).one_or_none()
        if not entity:
            raise ObjectNotFound()
        return cast(T, entity)

    def _get_first(
        self, model: Type[T], order_by: Any = None, **kwargs: Union[str, UUID, bool]
    ) -> T:
        query = self.db.session.query(model).filter_by(**kwargs)
        if order_by is not None:
            query = query.order_by(order_by)
        entity = query.first()
        if not entity:
            raise ObjectNotFound()
        return cast(T, entity)

    def _update_model_from_schema(self, model: T, schema: WasataBase) -> T:
        dictionary = schema.dict(exclude_unset=True)
        return self._update_model_from_dict(model, dictionary)

    def _update_model_from_dict(self, model: T, dictionary: Dict[str, Any]) -> T:
        for key, val in dictionary.items():
            setattr(model, key, val)
        self.db.flush()
        return model

    def _delete(self, model: UsersBase) -> None:  # type: ignore
        self.db.session.delete(model)
        self.db.flush()


class UserRepository(BaseRepository):
    def create(self, user_create: UserCreate) -> Users:
        user = Users(**user_create.dict())
        return self._create(user)

    def get(self, user_id: UUID) -> Users:
        return self._get_by_id(Users, user_id)

    # TODO catsh the error and do something
    def get_by_number(self, phone_number: str) -> Users | None:
        try:
            return self._get_one(Users, phone_number=phone_number)
        except ObjectNotFound:
            return None

    def get_by_email(self, email: str) -> Users | None:
        user = (
            self.db.session.query(Users)
            .filter((func.lower(Users.email) == email.lower()))
            .one_or_none()
        )

        if user is None:
            logging.info(f"There is no user with email: {email}")
            return None

        return cast(Users, user)

    def update(self, user: Users, user_update: UserUpdate) -> Users:
        return self._update_model_from_schema(user, user_update)


class AdminRepository(BaseRepository):
    def get_by_secret(self, api_secret_key: str) -> Admins:
        return self._get_one(Admins, api_secret_key=api_secret_key)

    def get_admin_usdt_price_by_username(self, username: str) -> float:
        admin = self._get_one(Admins, username=username)
        return admin.usdt_price

    def _get_usdt_price(self, model: Type[T], **kwargs: Union[str, UUID]) -> float:
        entity = self.db.session.query(model).filter_by(**kwargs).one_or_none()
        if not entity:
            raise ObjectNotFound()
        return entity.usdt_price

    def get(self, username: str) -> Union[Admins, None]:
        db_admin = (
            self.db.session.query(Admins)
            .filter((func.lower(Admins.username) == username.lower()))
            .one_or_none()
        )
        if db_admin is None:
            logging.info("You are new admin ... WELCOME")
            return None
        return cast(Admins, db_admin)

    def create(self, admin_create: AdminCreate) -> Admins:
        num_of_admins = self.db.session.query(Admins).count()
        if num_of_admins >= 1:
            raise Exception("maximum number of admins reached")
        admin_db = Admins(**admin_create.dict())
        return self._create(admin_db)

    def update(self, admins: Admins, admin_update: AdminUpdate) -> Admins:
        return self._update_model_from_schema(admins, admin_update)

    def delete(self, id: UUID) -> None:
        db_admin = self._get_by_id(Admins, id)
        self._delete(db_admin)
        self.db.commit()
