"""
Manages database connections and sessions.
"""
from typing import Any

from .models import Users, UsersBase, Admin

from .schemas import UserCreate, WasataBase, AdminCreate
from fastapi import Depends

from app.exceptions import ObjectNotFound, NotFound
import logging
from .database_engine import UserDB, get_user_db
from typing import TypeVar, Type, cast, Union, Dict
from uuid import UUID
from sqlalchemy import func

# ----------------------
# User functions
# ----------------------

T = TypeVar("T", bound=UsersBase)

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

    def _delete(self, model: UsersBase) -> None:
        self.db.session.delete(model)
        self.db.flush()


class UserRepository(BaseRepository):
    def create(self, user_create: UserCreate) -> Users:
        user = Users(**user_create.dict())
        return self._create(user)

    def get(self, user_id: UUID) -> Users:
        return self._get_by_id(Users, user_id)

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

    # def update(
    #         self, user: Users, user_update: Union[UserUpdate, UserUpdateEmail]
    # ) -> Users:
    #     return self._update_model_from_schema(user, user_update)


class AdminRepository(BaseRepository):
    def get_by_email(self, email: str) -> Admin | None:
        admin = (
            self.db.session.query(Admin)
            .filter((func.lower(Admin.admin_email) == email.lower()))
            .one_or_none()
        )
        if admin is None:
            logging.info(f"There is no user with email: {email}")
            return None

        return cast(Admin, admin)

    def create(self, admin_create: AdminCreate) -> Admin:
        admin = Admin(**admin_create.dict())
        return self._create(admin)

    def update_price(self, admin_value, new_price) -> Admin | None:
        admin = (
            self.db.session.query(Admin).filter_by(Admin.value == admin_value).first()
        )
        if admin:
            admin.admin_price = new_price
            self.db.commit()
            self.db.session.refresh(admin)
            self.db.flush()
            return admin
        else:
            logger.error("You are not the admin please try again")
            raise NotFound
