import enum
import hashlib
import json
import uuid
from datetime import datetime
from typing import Any

from pydantic import Field
from sqlalchemy import BigInteger, String, Integer, Boolean, DateTime, func, JSON, Enum, ForeignKey, case
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship, column_property
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.enums import TarifType


class DBModel(DeclarativeBase):
    pass


class Users(DBModel):
    __tablename__ = 'Users'

    # def __init__(self, **kw: Any):
    #     super().__init__(**kw)
    #     self.current_date = func.now()
    #     if self.current_date == self.purchase_date:
    #         if self.tarif_of_user == TarifType.FREE:
    #             self.limit_urls = 20
    #             self.limit_images = 5
    #         elif self.tarif_of_user == TarifType.PRIVATE:
    #             self.limit_urls = 100
    #             self.limit_images = 30
    #         else:
    #             self.limit_urls = -1
    #             self.limit_images = 200

    login: Mapped[str] = mapped_column(String(100), nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(String(200), nullable=True, unique=False)

    telegram: Mapped[int] = mapped_column(BigInteger, nullable=True)
    yandex: Mapped[bool] = mapped_column(Boolean, nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)

    limit_urls: Mapped[int] = mapped_column(Integer, default=20)

    purchase_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    tarif_of_user: Mapped[enum] = mapped_column(ENUM(TarifType), default=TarifType.FREE)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), nullable=False)

    def quota_images(self):
        if func.now() > self.purchase_date and self.tarif_of_user == TarifType.PRIVATE:
            self.quota_images = 30
        if func.now() > self.purchase_date and self.tarif_of_user == TarifType.FREE:
            self.quota_images = 5
        if func.now() > self.purchase_date and self.tarif_of_user == TarifType.PRO:
            self.quota_images = 200
        return self.quota_images




class Tarif(DBModel):
    __tablename__ = 'Tarif'

    name: Mapped[enum] = mapped_column(ENUM(TarifType), primary_key=True)

    limit_urls_per_month: Mapped[int] = mapped_column(Integer)
    limit_images_per_month: Mapped[int] = mapped_column(Integer)

    price_per_month: Mapped[int] = mapped_column(Integer)
    price_per_year: Mapped[int] = mapped_column(Integer)
