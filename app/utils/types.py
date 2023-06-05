import uuid
from typing import Any, Type

from app.exceptions import WasataNotImplemented
from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID


class GUID(TypeDecorator):  # type: ignore
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    Taken from https://docs.sqlalchemy.org/en/14/core/custom_types.html#backend-agnostic-guid-type

    """

    @property
    def python_type(self) -> Type[uuid.UUID]:
        return uuid.UUID

    def process_literal_param(self, value: Any, dialect: Any) -> str:
        raise WasataNotImplemented()

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Any) -> Any:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return "%.32x" % uuid.UUID(value).int  # pylint: disable=C0209
        return "%.32x" % value.int  # pylint: disable=C0209

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value
