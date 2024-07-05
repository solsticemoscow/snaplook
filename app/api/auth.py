# from typing import Annotated
#
# from fastapi import APIRouter, Depends
# from fastapi.security import OAuth2PasswordRequestForm
# from starlette.status import HTTP_200_OK
#
# from app.core.schemas import Token
# from app.services.auth import AuthService, get_auth_service
# # from app.services.auth_keycloak import keycloak_process
#
# router = APIRouter()
#
#
# @router.post(
#     path="/login",
#     status_code=HTTP_200_OK,
#     summary="Log in to system",
# )
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     auth_service: AuthService = Depends(get_auth_service),
# ) -> Token:
#     """Login with OAuth2 Form"""
#     return await auth_service.login(form_data)
#
# # @router.post(
# #     path="/login",
# #     status_code=HTTP_200_OK,
# #     summary="Log in to system",
# # )
# # async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
# #     print(form_data.username)
# #     return await keycloak_process(form_data.username, form_data.password)
