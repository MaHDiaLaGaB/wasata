import uuid
import re
from enum import Enum

from pydantic import BaseModel, validator, Extra, Field
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
    phone_number: str
    tokens: float
    _invoice_id: uuid.UUID
    user_status: StatusEntity = Field(default=StatusEntity.INACTIVE)

    class Config:
        exclude = ["invoice_id"]

    @validator("phone_number")
    def validate_phone_number(cls, phone_number: str) -> str:
        pattern = r"^(092|091|094|095)\d{7}$"
        match = re.match(pattern, phone_number)
        if not match:
            raise ValueError("phone number not looks rights")
        return phone_number

    @validator("tokens")
    def validate_tokens(cls, tokens: float) -> float:
        if tokens <= 0:
            raise ValueError("Tokens must be greater than 0")
        return tokens

    @property
    def user_state(self) -> str:
        # Assuming StatusEntity has string values associated with its members
        return self.user_status.value

    @user_state.setter
    def user_state(self, value: str) -> None:
        # Convert the incoming string to a StatusEntity enum, ensuring it's a valid enum member
        try:
            self.user_status = StatusEntity(value)
        except ValueError:
            raise ValueError(f"{value} is not a valid status")


class UserUpdate(WasataBase):
    price: Optional[float] = None
    tokens: Optional[float] = None
    status: Optional[StatusEntity] = None


class UserGet(UserCreate):
    created_at: datetime
    price: float
    total_price: float
    _user_status: StatusEntity


class AdminCreate(BaseModel):
    username: str
    password: str = Field(..., write_only=True)
    usdt_price: float


class Admins(BaseModel):
    username: str
    usdt_price: float
    api_secret_key: str


class AdminUpdate(BaseModel):
    usdt_price: float | None

# class AdminInDB(AdminCreate):
#     id: int
#     password: str = Field(..., write_only=True)
#     api_secret_key: str
#
#     class Config:
#         orm_mode = True
