import enum
import hashlib
import json
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, String, Integer, Boolean, DateTime, func, JSON, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

from app.models.enums import TarifType


class DBModel(DeclarativeBase):
    pass


class Users(DBModel):
    __tablename__ = 'Users'

    login: Mapped[str] = mapped_column(String(100), nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(String(200), nullable=True, unique=False)

    telegram: Mapped[int] = mapped_column(BigInteger, nullable=True)
    yandex: Mapped[bool] = mapped_column(Boolean, nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), nullable=False)

    urls_per_month: Mapped[int] = mapped_column(Integer, default=20)
    images_per_month: Mapped[int] = mapped_column(Integer, default=5)

    tarif_of_user: Mapped[enum] = mapped_column(ENUM(TarifType), default=TarifType.FREE)
    #
    # def __init__(self, **kw: Any):
    #     super().__init__(**kw)
    #     self.limit_urls = self.urls_per_month
    #     self.limit_images = self.images_per_month
    #     self.last_purchase_date = self.last_purchase_date
    #
    # @property
    # def remaining_limit(self):
    #     current_date = func.now()
    #     if current_date.month != self.last_purchase_date.month:
    #         self.last_purchase_date = current_date
    #     return self.limit_urls, self.limit_images
    #
    # def run_url(self):
    #     if self.limit_urls > self.urls_per_month:
    #         raise ValueError("Limit of urls exceeded.")
    #     else:
    #         self.urls_per_month -= 1
    #
    # def run_image(self):
    #     if self.limit_images > self.images_per_month:
    #         raise ValueError("Limit of images exceeded.")
    #     else:
    #         self.images_per_month -= 1





class Tarif(DBModel):
    __tablename__ = 'Tarif'

    name: Mapped[enum] = mapped_column(ENUM(TarifType), primary_key=True)

    limit_urls_per_month: Mapped[int] = mapped_column(Integer)
    limit_images_per_month: Mapped[int] = mapped_column(Integer)

    price_per_month: Mapped[int] = mapped_column(Integer)
    price_per_year: Mapped[int] = mapped_column(Integer)







