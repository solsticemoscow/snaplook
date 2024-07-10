from typing import Optional
from datetime import datetime
import uuid

from pydantic import BaseModel, EmailStr


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        underscore_attrs_are_private = True
        use_enum_values = True


class User(BaseSchema):
    login: str = None
    password: str = None
    email: EmailStr = None
    telegram: Optional[int] = None
    yandex: Optional[bool] = None
    is_active: bool = None
    created_at: datetime = None


class UserChange(BaseSchema):
    password: Optional[str] | None = None
    email: Optional[EmailStr] | None = None


class PaymentRequest(BaseSchema):
    login: str
    sum: int = 10
    description: str = 'Test payment.'

class RefundRequest(BaseSchema):
    login: str
    sum: int = 10
    payment_id: str = 'Test refund.'
