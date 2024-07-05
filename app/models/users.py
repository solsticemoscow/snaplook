import uuid

import sqlalchemy as sa
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import Session, relationship, backref, DeclarativeBase
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.core.security import get_hashed_password, verify_password


class DBModel(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass


class User(DBModel):
    __tablename__ = 'users'

    id = sa.Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    number = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    login = sa.Column(sa.String(200), index=True, unique=True, nullable=False)
    password_hash = sa.Column(sa.String(200), nullable=False)


    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), nullable=False)



    @property
    def password(self):
        raise AttributeError(f'Password property is write-only')

    @password.setter
    def password(self, password_string: str):
        self.password_hash = get_hashed_password(password_string)

    @classmethod
    def authenticate(cls, db_session: Session, login: str, password: str):
        try:
            user = cls.get_by_login(db_session, login=login)
        except (NoResultFound, MultipleResultsFound):
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @classmethod
    def get_by_login(cls, db_session: Session, login: str, active_only=True):
        users_query = db_session.query(cls).filter_by(login=login)
        if active_only:
            users_query = users_query.filter_by(is_active=True)
        return users_query.one()

    @classmethod
    def get_by_id(cls, db_session: Session, id: int, active_only=True):
        user = db_session.get(cls, id)
        if active_only:
            return user if user.is_active else None
        else:
            return user
