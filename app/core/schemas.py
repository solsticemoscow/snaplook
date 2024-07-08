from typing import Optional
from datetime import datetime
import uuid

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        underscore_attrs_are_private = True
        use_enum_values = True


class User(BaseSchema):
    unique_id: str
    login: str
    password: str
    email: str
    telegram: Optional[int]
    yandex: Optional[bool]
    is_active: bool
    created_at: datetime


