"""
Contains your database models (e.g., SQLAlchemy ORM models) and their relationships.
"""
from enum import Enum
import logging
from dotenv import load_dotenv
import uuid
from sqlalchemy.orm import registry
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy_utils.types.email import EmailType
from sqlalchemy_utils.types import UUIDType
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
class Users(UsersBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), unique=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(EmailType)
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
    id = Column(Integer, primary_key=True)
    admin_email = Column(String)
    admin_username = Column(String)
    admin_password = Column(String)
    admin_price = Column(Integer)

    def __init__(self, admin_email, admin_username, admin_password, admin_price):
        self.admin_email = admin_email
        self.admin_username = admin_username
        self.admin_password = generate_password_hash(admin_password)
        self.admin_price = admin_price

    def check_password(self, password):
        return check_password_hash(self.admin_password, password)

