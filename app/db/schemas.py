import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr, validator, Extra, Field
from typing import Optional
from datetime import datetime


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
        extra = Extra.allow
        use_enum_values = True
        anystr_strip_whitespace = True
        validate_all = True
        validate_assignment = True
        allow_inf_nan = False


class UserCreate(WasataBase):
    name: str
    invoice_id: uuid.UUID
    email: EmailStr
    phone_number: int
    tokens: float

    @validator("name")
    def validate_name(cls, name: str) -> str:
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return name

    @validator("phone_number")
    def validate_phone_number(cls, phone_number: int) -> int:
        if len(str(phone_number)) != 9:
            raise ValueError("Phone number must be exactly 9 digits long")
        return phone_number

    @validator("tokens")
    def validate_tokens(cls, tokens: float) -> float:
        if tokens <= 0:
            raise ValueError("Tokens must be greater than 0")
        return tokens


class UserUpdate(WasataBase):
    price: Optional[float] = None
    tokens: Optional[float] = None
    status: Optional[StatusEntity] = None


class UserGet(UserCreate):
    created_at: datetime
    price: float
    status: str = StatusEntity.INACTIVE


class AdminCreate(WasataBase):
    username: str
    password: str = Field(..., write_only=True)


class AdminUpdate(WasataBase):
    username: Optional[str]
    password: str = Field(..., write_only=True)


# class AdminInDB(AdminCreate):
#     id: int
#     api_secret_key: str
#
#     class Config:
#         orm_mode = True
