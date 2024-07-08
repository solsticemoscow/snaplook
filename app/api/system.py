
import os


from fastapi import APIRouter, Depends, UploadFile, File
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.config import settings
from app.services.m_openai import ClassOpenAI
from app.services.m_utils import UtilsClass
from app.services.m_wb import ClassWB

router = APIRouter()

@router.get(path='/from_url', summary='Get OpenAI response from url.', status_code=200)
async def get_url(
    url: str,
    # _: Annotated[User, Depends(get_current_user)],
):
    all_results = []

    try:
        response = await UtilsClass.add_dialog_stylist(content=url, role='user')

        result: str = await ClassOpenAI.get_text(response)

        result_list: list = result.replace('\n', '').rsplit(',')


        for item in result_list:
            all_results.append(ClassWB.get_all_products_in_search_result(key_word=item)[:3])


        return JSONResponse(
            status_code=HTTP_200_OK,
            content=all_results,
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Error to proceed url: {e}',
        )





@router.post(path='/from_image', summary='Get OpenAI response from image.', status_code=200)
async def get_image(
    file: UploadFile = File(...),
    # _: Annotated[User, Depends(get_current_user)],
):
    all_results = []
    filepath = settings.ROOT_PATH + f"/files/{file.filename}"

    try:
        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())


        result: str = await ClassOpenAI.get_vision(image_path=filepath)
        result_list: list = result.replace('\n', '').rsplit(',')

        for item in result_list:
            all_results.append(ClassWB.get_all_products_in_search_result(key_word=item)[:8])

        return JSONResponse(
                status_code=HTTP_200_OK,
                content=all_results,
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Error to proceed image: {e}',
        )
    finally:
        os.remove(filepath)

