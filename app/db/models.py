"""
Contains your database models (e.g., SQLAlchemy ORM models) and their relationships.
"""
from functools import partial
import re
import os
from enum import Enum
import logging
from dotenv import load_dotenv
from sqlalchemy.orm import declared_attr
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

load_dotenv()

logger = logging.getLogger(__name__)

_snake_1 = partial(re.compile(r'(.)((?<![^A-Za-z])[A-Z][a-z]+)').sub, r'\1_\2')
_snake_2 = partial(re.compile(r'([a-z0-9])([A-Z])').sub, r'\1_\2')

# Database configurations
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")

SU_DSN = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

class StatusEntity(str, Enum):
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    BANNED = "banned"
    BLOCKED = "blocked"


# ---------------------------------------
# Convert to snake casing (for DB models)
# ---------------------------------------
def snake_case(string: str) -> str:
    return _snake_2(_snake_1(string)).casefold()


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)

    @classmethod
    def by_uuid(self, _uuid: uuid_pkg.UUID):
        with Session(get_engine()) as session:
            q = select(self).where(self.uuid == _uuid)
            org = session.exec(q).first()
            return org if org else None

    def update(self, o: Union[SQLModel, dict] = None):
        if not o:
            raise ValueError("Must provide a model or dict to update values")
        o = o if isinstance(o, dict) else o.dict(exclude_unset=True)
        for key, value in o.items():
            setattr(self, key, value)

        # save and commit to database
        with Session(get_engine()) as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self):
        with Session(get_engine()) as session:
            self.status = StatusEntity.DELETED
            self.updated_at = datetime.utcnow()
            session.add(self)
            session.commit()
            session.refresh(self)

    @classmethod
    def create(self, o: Union[SQLModel, dict] = None):
        if not o:
            raise ValueError("Must provide a model or dict to update values")

        with Session(get_engine()) as session:
            obj = self.from_orm(o) if isinstance(o, SQLModel) else self(**o)
            session.add(obj)
            session.commit()
            session.refresh(obj)

        return obj


# ==========================
# Tracking the user activity
# ==========================
class MyModel(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: uuid_pkg.UUID = Field(unique=True, default_factory=uuid_pkg.uuid4)
    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    tokens: condecimal(max_digits=9, decimal_places=4) = Field(default=000.000000)
    price: condecimal(max_digits=9, decimal_places=6) = Field(default=000.000000)
    status: str = Field(default=StatusEntity.ACTIVE)


# ==================
# Database functions
# ==================
def get_engine(dsn: str = SU_DSN):
    return create_engine(dsn)


def get_session():
    with Session(get_engine()) as session:
        yield session


def create_db():
    logger.info("...Enabling pgvector and creating database tables")
    BaseModel.metadata.create_all(get_engine(dsn=SU_DSN))
    create_user_permissions()


def create_user_permissions():
    session = Session(get_engine(dsn=SU_DSN))
    # grant access to entire database and all tables to user DB_USER
    query = f"GRANT ALL PRIVILEGES ON DATABASE TO {POSTGRES_USER};"
    session.execute(query)
    session.commit()
    session.close()


def drop_db():
    BaseModel.metadata.drop_all(get_engine(dsn=SU_DSN))


if __name__ == "__main__":
    create_db()
