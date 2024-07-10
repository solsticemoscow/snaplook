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
from app.core.schemas import User, UserChange, PaymentRequest, RefundRequest
from app.core.db import db_session
from app.models import Users
from app.services.m_youkassa import ClassYK

router = APIRouter()


@router.post(
    path="/create_payment",
    status_code=HTTP_200_OK,
    summary='Logic for create payment.'
)
async def create_payment(
        payment_request: PaymentRequest,
        db_session: AsyncSession = Depends(db_session),
        # _: Annotated[User, Depends(get_current_user)],
):
    async with db_session:
        stmt = select(Users).where(Users.login == payment_request.login)
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            result = ClassYK.create_payment(payment_request.sum, payment_request.description)
            print(result)
            return JSONResponse(
                status_code=HTTP_200_OK,
                content={"payment_id": result[0], "confirmation_url": result[1]}
            )
        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User not found in DB.',
            )


@router.get(
    path="/get_payment_status",
    status_code=HTTP_200_OK,
    summary='Logic for get payment.'
)
async def get_payment_status(
        payment_id: str,
        # _: Annotated[User, Depends(get_current_user)],
):
    payment_status = ClassYK.get_payment(payment_id)
    print(payment_status)
    return {"payment_status": payment_status}


@router.post(
    path="/create_refund",
    status_code=HTTP_200_OK,
    summary='Logic for create refund.'
)
async def create_refund(
        refund_request: RefundRequest,
        db_session: AsyncSession = Depends(db_session),
        # _: Annotated[User, Depends(get_current_user)],
):
    async with db_session:
        stmt = select(Users).where(Users.login == refund_request.login)
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            refund_result = ClassYK.create_refund(refund_request.sum, refund_request.payment_id)
            return {"refund_result": refund_result}
        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User not found in DB.',
            )


@router.get(
    path="/get_refund_status",
    status_code=HTTP_200_OK,
    summary='Logic for get refund.'
)
async def get_refund_status(
        refund_id: str,
        # _: Annotated[User, Depends(get_current_user)],
):
    refund_status = ClassYK.get_refund(refund_id)
    return {"refund_status": refund_status}
