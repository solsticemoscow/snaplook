import hashlib
import uuid
from typing import Annotated, Optional, Union

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy import insert, delete, select, or_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.core.auth import get_current_user
from app.core.schemas import User, UserChange
from app.core.db import db_session
from app.models import Users

router = APIRouter()


@router.post(
    path='/create_user',
    response_model=User,
    status_code=HTTP_200_OK,
    summary='Add new user',
)
async def create_user(
        user: User,
        # _: Annotated[Users, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),

) -> Union[User, HTTP_400_BAD_REQUEST]:


    password_hash = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

    async with db_session:
        stmt = select(Users).filter(or_(Users.login == user.login, Users.email == user.email))
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User already created.',
            )
        else:
            stmt = insert(Users).values(
                login=user.login,
                password=password_hash,
                email=user.email
            )
            await db_session.execute(statement=stmt)
            await db_session.commit()

            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly created: {user}',
            )


@router.patch(
    path='/update_user',
    summary='Change user',
    response_model=User,
    status_code=HTTP_200_OK,
)
async def update_user(
        user: User,
        login: str = None,
        email: str = None,
        # _: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),
) -> Union[User, HTTP_400_BAD_REQUEST]:

    if not (login or email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Must fill login or email field.',
        )

    async with db_session:
        stmt = select(Users).filter(or_(Users.login == login, Users.email == email))
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            stmt = update(Users).where(or_(Users.login == login, Users.email == email)).values(user.model_dump(exclude_unset=True))
            await db_session.execute(statement=stmt)
            await db_session.commit()

            # if user.password:
            #     stmt = update(Users).where(or_(Users.login == login, Users.email == email)).values(
            #         password=user.password)
            #     await db_session.execute(statement=stmt)
            #     await db_session.commit()
            # elif user.email:
            #     stmt = update(Users).where(or_(Users.login == login, Users.email == email)).values(
            #         email=user.email)
            #     await db_session.execute(statement=stmt)
            #     await db_session.commit()
            # else:
            #     stmt = update(Users).where(or_(Users.login == login, Users.email == email)).values(
            #         email=user.email, password=user.password)
            #     await db_session.execute(statement=stmt)
            #     await db_session.commit()

            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly changed: {user}',
            )

        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User not found in DB.',
            )



@router.delete(
    path='/delete',
    status_code=HTTP_200_OK,
    summary='Delete user',
)
async def delete_user(
        login: str,
        # _: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),
):
    async with db_session:
        stmt = select(Users).where(Users.login == login)
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            stmt = delete(Users).where(Users.login == login)
            await db_session.execute(statement=stmt)
            await db_session.commit()


            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly deleted: {login}',
            )

        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User not found in DB.',
            )