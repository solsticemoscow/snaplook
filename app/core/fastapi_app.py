from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.router import router as api_router
from files.t1 import User


def create_application():

    app = FastAPI(title='Snap Look')
    app.include_router(api_router)

    @app.get('/')
    async def redirect():
        response = RedirectResponse(url='http://localhost:8444/docs')
        return response

    return app

app = create_application()

def get_application():
    global app
    if app is None:
        app = create_application()
    return app
