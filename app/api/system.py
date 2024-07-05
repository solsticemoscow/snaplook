from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.core.auth import get_current_user
from app.core.db import async_db_session
from app.models.users import User
from app.services.m_openai import ClassOpenAI
from app.services.m_utils import UtilsClass

router = APIRouter()



@router.get(path='/get_url', summary='Get OpenAI response from url.', status_code=200)
async def get_url(
    url: str,
    _: Annotated[User, Depends(get_current_user)],
):
    try:
        response = await UtilsClass.add_dialog_stylist(content=url, role='user')
        result = await ClassOpenAI.get_text(response)
        return result

    except Exception as e:
        print(e)
        return e

@router.get(path='/get_image', summary='Get OpenAI response from image.', status_code=200)
async def get_image(
    base64_image: str,
    _: Annotated[User, Depends(get_current_user)],
):
    try:
        print(base64_image)

        return ClassOpenAI.get_vision(base64_image=base64_image)

    except Exception as e:
        print(e)
        return e

