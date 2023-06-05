from enum import Enum
import uuid
from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr, PrivateAttr, Field


class StatusEntity(str, Enum):
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    BANNED = "banned"
    BLOCKED = "blocked"


class WasataBase(BaseModel):
    class Config:
        orm_mode = True
        extra = "forbid"
        use_enum_values = True
        anystr_strip_whitespace = True
        validate_all = True
        validate_assignment = True
        allow_inf_nan = False


class UserCreate(WasataBase):
    name: str
    email: EmailStr
    phone_number: int
    tokens: float
    wallet_address: str


class UserGet(UserCreate):
    uuid: uuid.UUID
    status: Union[StatusEntity, None] = StatusEntity.INACTIVE
    created_at: datetime
    price: float


class AdminCreate(WasataBase):
    admin_email: EmailStr
    admin_username: str
    admin_password: str
    admin_price: float
    _value: str = PrivateAttr()
    value: str = Field(alias="_value")
