"""
Contains your database models (e.g., SQLAlchemy ORM models) and their relationships.
"""
from enum import Enum
import logging
from dotenv import load_dotenv
import uuid
from sqlalchemy.orm import declared_attr, registry
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy_utils.types.email import EmailType
from sqlalchemy_utils.types import UUIDType
from sqlalchemy.dialects.postgresql import UUID
from pydantic import EmailStr, condecimal
from datetime import datetime
from typing import Union
import uuid as uuid_pkg
from sqlmodel import (
    create_engine,
    SQLModel,
    Session,
    select,
    Field,
)

from app.core.config import config
from app.utils.helper_function import snake_case
from app.db.schemas import StatusEntity

load_dotenv()

logger = logging.getLogger(__name__)


SU_DSN = config.DATABASE_URI

users_mapper_registry = registry()

UsersBase = users_mapper_registry.generate_base()


# class BaseModel(SQLModel):
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return snake_case(cls.__name__)
#
#     @classmethod
#     def by_uuid(self, _uuid: uuid_pkg.UUID):
#         with Session(get_engine()) as session:
#             q = select(self).where(self.uuid == _uuid)
#             org = session.exec(q).first()
#             return org if org else None
#
#     def update(self, o: Union[SQLModel, dict] = None):
#         if not o:
#             raise ValueError("Must provide a model or dict to update values")
#         o = o if isinstance(o, dict) else o.dict(exclude_unset=True)
#         for key, value in o.items():
#             setattr(self, key, value)
#
#         # save and commit to database
#         with Session(get_engine()) as session:
#             session.add(self)
#             session.commit()
#             session.refresh(self)
#
#     def delete(self):
#         with Session(get_engine()) as session:
#             self.status = StatusEntity.DELETED
#             self.updated_at = datetime.utcnow()
#             session.add(self)
#             session.commit()
#             session.refresh(self)
#
#     @classmethod
#     def create(self, o: Union[SQLModel, dict] = None):
#         if not o:
#             raise ValueError("Must provide a model or dict to update values")
#
#         with Session(get_engine()) as session:
#             obj = self.from_orm(o) if isinstance(o, SQLModel) else self(**o)
#             session.add(obj)
#             session.commit()
#             session.refresh(obj)
#
#         return obj


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
# Admin Info
# ==========================
# class Admin(BaseModel, table=True):
#     pass


# ==================
# Database functions
# ==================
# def get_engine(dsn: str = SU_DSN):
#     return create_engine(dsn)
#
#
# def get_session():
#     with Session(get_engine()) as session:
#         yield session
#
#
# def create_db():
#     logger.info("...Enabling pgvector and creating database tables")
#     BaseModel.metadata.create_all(get_engine(dsn=SU_DSN))
#     create_user_permissions()
#
#
# def create_user_permissions():
#     session = Session(get_engine(dsn=SU_DSN))
#     # grant access to entire database and all tables to user DB_USER
#     query = f"GRANT ALL PRIVILEGES ON DATABASE TO {config.POSTGRES_USER};"
#     session.execute(query)
#     session.commit()
#     session.close()
#
#
# def drop_db():
#     BaseModel.metadata.drop_all(get_engine(dsn=SU_DSN))

#
# if __name__ == "__main__":
#     create_db()
