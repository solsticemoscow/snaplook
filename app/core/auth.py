
from typing import Annotated


from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/auth/login',
    scheme_name='JWT'
)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return token








