
from fastapi import APIRouter
from pydantic_core import Url

from app.services.m_openai import ClassOpenAI
from app.services.m_utils import UtilsClass

router = APIRouter()


@router.get(path='/get_url', summary='Get OpenAI response from url.', status_code=200)
async def get_url(
    url: str
):
    try:
        response = await UtilsClass.add_dialog_stylist(content=url, role='user')

        result = await ClassOpenAI.get_text(response)

        print(result)

        return result

    except Exception as e:
        print(e)
        return e

@router.get(path='/get_image', summary='Get OpenAI response from image.', status_code=200)
async def get_image(
    base64_image: str
) -> str:
    try:
        print(base64_image)

        return ClassOpenAI.get_vision(base64_image=base64_image)

    except Exception as e:
        print(e)
        return e

