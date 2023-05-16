from enum import Enum
import uuid
from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr, PositiveFloat


class StatusEntity(str, Enum):
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    BANNED = "banned"
    BLOCKED = "blocked"


class UserBase(BaseModel):
    name: str
    email: EmailStr
    tokens: PositiveFloat

    # @validator('tokens', pre=True)
    # def parse_tokens(cls, value):
    #     return round(float(value), 4)
    #
    # class Config:
    #     validate_assignment = True


class User(UserBase):
    session: uuid.UUID
    status: Union[StatusEntity, None]
    date: datetime
