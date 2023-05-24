"""
Contains your database models (e.g., SQLAlchemy ORM models) and their relationships.
"""
from enum import Enum
import logging
from dotenv import load_dotenv
import uuid
from typing import TYPE_CHECKING, Any
from cryptography.fernet import Fernet
from app.utils.types import GUID
from sqlalchemy.orm import registry
from sqlalchemy import Column, String, DateTime, Numeric, LargeBinary, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
if TYPE_CHECKING:
    # This makes hybrid_property's have the same typing as normal property until stubs are improved.
    hybrid_property = property  # pylint: disable=C0103
else:
    from sqlalchemy.ext.hybrid import hybrid_property


from datetime import datetime

from app.core.config import config


load_dotenv()

logger = logging.getLogger(__name__)


SU_DSN = config.DATABASE_URI

users_mapper_registry = registry()

UsersBase = users_mapper_registry.generate_base()

admin_secret_fernet_instance = Fernet(bytes.fromhex(config.SECRETS_ENCRYPTION_KEY))


# ==========================
# Tracking the user activity
# ==========================
class Users(UsersBase):
    __tablename__ = 'users'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    _uuid = Column(GUID, unique=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    tokens = Column(Numeric(9, 4))
    price = Column(Numeric(9, 4))
    status = Column(String, default='active')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ==========================
# Tracking the Admin activity
# ==========================

class Admin(UsersBase):
    __tablename__ = 'admin'
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    admin_email = Column(String, nullable=False, unique=True)
    admin_username = Column(String)
    admin_password = Column(String)
    admin_price = Column(Numeric(9, 4))
    _value = Column("private_key", LargeBinary, nullable=False)

    @hybrid_property
    def value(self) -> str:
        decrypted = admin_secret_fernet_instance.decrypt(self._value)
        return decrypted.decode(encoding="utf-8")

    @value.setter
    def value(self, value: str) -> None:
        value_bytes = bytes(value, "utf-8")
        self._value = admin_secret_fernet_instance.encrypt(value_bytes)

    def __init__(self, admin_email, admin_username, admin_password, admin_price, **kwargs: Any):
        self.admin_email = admin_email
        self.admin_username = admin_username
        self.admin_password = generate_password_hash(admin_password)
        self.admin_price = admin_price
        value = kwargs["value"]
        del kwargs["value"]
        super().__init__(**kwargs)
        self.value = value

    __table_args__ = (UniqueConstraint("admin_username", "admin_price"),)

    def check_password(self, password):
        return check_password_hash(self.admin_password, password)

