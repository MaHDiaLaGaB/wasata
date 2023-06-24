"""
Contains your database models (e.g., SQLAlchemy ORM models) and their relationships.
"""
import logging
import uuid

from dotenv import load_dotenv
from typing import Dict, Any
from cryptography.fernet import Fernet
from app.type import GUID
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, ForeignKey
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from app.core.config import config

load_dotenv()

logger = logging.getLogger(__name__)

SU_DSN = config.DATABASE_URI

users_mapper_registry = registry()

UsersBase = users_mapper_registry.generate_base()


# ==========================
# Tracking the user activity
# ==========================
class Users(UsersBase):  # type: ignore
    __tablename__: str = "users"

    id = Column(GUID, primary_key=True, unique=True, default=uuid.uuid4)
    invoice_id = Column(GUID, unique=True)
    phone_number = Column(BigInteger, nullable=False, unique=False)
    created_at = Column(DateTime, default=datetime.now)
    tokens = Column(Numeric(9, 4))
    price = Column(Numeric(9, 4))
    user_status = Column(String)
    admin_id = Column(GUID, ForeignKey("admins.id"))

    admin = relationship("Admins", back_populates="users")

    def __init__(self, **kwargs: Dict[str, int | GUID | DateTime | Numeric]) -> None:
        super().__init__(**kwargs)


# ==========================
# Tracking the Admin activity
# ==========================


class Admins(UsersBase):  # type: ignore
    __tablename__: str = "admins"

    id = Column(GUID, primary_key=True, unique=True, default=uuid.uuid4)
    username = Column(String(64), index=True, unique=True)
    _password_hash = Column("password_hash", String(128))
    api_secret_key = Column(String(128))
    usdt_price = Column(Numeric())

    users = relationship("Users", back_populates="admin")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.api_secret_key = self.generate_api_secret_key()

    @property
    def password(self) -> None:
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str) -> None:
        self._password_hash = generate_password_hash(password)

    def generate_api_secret_key(self) -> str:
        key = bytes.fromhex(config.SECRETS_ENCRYPTION_KEY)
        f = Fernet(key)
        return f.encrypt(secrets.token_bytes(16)).decode()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password_hash, password)
