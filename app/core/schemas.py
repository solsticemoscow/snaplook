import enum
from typing import Optional
from datetime import datetime
import uuid

from pydantic import BaseModel, EmailStr
from sqlalchemy import func

from app.models.enums import TarifType


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

    limit_urls: int = 20
    limit_images: int = 5
    purchase_date: datetime = func.now()
    tarif_of_user: TarifType = TarifType.FREE


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
