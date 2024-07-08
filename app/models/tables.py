import enum
import hashlib
import json
import uuid
from datetime import datetime


from sqlalchemy import BigInteger, String, Integer, Boolean, DateTime, func, JSON, Enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

from app.models.enums import TarifType


class DBModel(DeclarativeBase):
    pass


class Users(DBModel):
    __tablename__ = 'Users'

    unique_id: Mapped[str] = mapped_column(String(100), primary_key=True)

    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=True, unique=False)

    telegram: Mapped[int] = mapped_column(BigInteger, nullable=True)
    yandex: Mapped[bool] = mapped_column(Boolean, nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), nullable=False)



class Tarif(DBModel):
    __tablename__ = 'Tarif'

    id: Mapped[str] = mapped_column(String(100), primary_key=True)

    name: Mapped[enum] = mapped_column(ENUM(TarifType))

    limit_url: Mapped[int] = mapped_column(Integer)
    limit_image: Mapped[int] = mapped_column(Integer)

    duration: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    price: Mapped[int] = mapped_column(Integer)







