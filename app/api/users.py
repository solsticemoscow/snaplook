import hashlib
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import insert, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.core.auth import get_current_user
from app.core.schemas import User
from app.core.db import db_session
from app.models import Users

router = APIRouter()


@router.post(
    path='/create_user',
    status_code=HTTP_201_CREATED,
    summary='Add new user',
)
async def create_user(
        user: User,
        # _: Annotated[Users, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),

):
    try:

        password_hash = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

        async with db_session:
            stmt = insert(Users).values(
                unique_id=str(uuid.uuid4()),
                login=user.login,
                password=password_hash,
                email=user.email
            )
            await db_session.execute(statement=stmt)
            await db_session.commit()

        return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User {user.login} successfuly created.',
            )

    except Exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'User {user.login} already created.',
        )


@router.patch(
    path='/update_user/{user_login}',
    summary='Change user'
)
async def update_user(
        user_login: str,
        # _: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),
):
    try:

        password_hash = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

        async with db_session:
            stmt = insert(Users).values(
                unique_id=str(uuid.uuid4()),
                login=user.login,
                password=password_hash,
                email=user.email
            )
            await db_session.execute(statement=stmt)
            await db_session.commit()

        return f'User {user.login} successfuly created.'

    except Exception:
        return f'User {user.login} already created.'


@router.delete(
    path='/delete',
    status_code=HTTP_200_OK,
    summary='Delete user',
)
async def delete_user(
        user_login: str,
        # _: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),
):
    try:
        async with db_session:
            stmt = select(Users).where(
                login=user_login,
            )
            result = await db_session.execute(statement=stmt)
            user = result.one_or_none()
            if user:
                stmt = delete(Users).where(
                    login=user_login,
                )
                await db_session.execute(statement=stmt)
                await db_session.commit()

                return f'User {user_login} successfuly deleted.'
            else:
                return f'User {user_login} not found.'

    except Exception as e:
        return e
