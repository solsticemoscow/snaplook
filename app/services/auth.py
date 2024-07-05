from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime

from app.core.db import db_session

from app.config import settings




reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl='/api/auth/login',
    scheme_name="JWT"
)


def get_current_user(
            db_session: Session = Depends(db_session),
            token: str = Depends(reusable_oauth2)
) -> m.User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = db_session.query(User).filter_by(login=payload['sub']).one_or_none()
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')

    return user
