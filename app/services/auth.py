# import re
#
# import requests
# from fastapi import Depends, HTTPException, Request
# from fastapi.security import OAuth2PasswordRequestForm
# from starlette.status import (
#     HTTP_400_BAD_REQUEST,
#     HTTP_401_UNAUTHORIZED,
#     HTTP_403_FORBIDDEN,
#     HTTP_404_NOT_FOUND,
# )
#
#
# from app.core.auth import reusable_oauth2
#
#
#
# class AuthService:
#     """Service class which provides authentification and authorization operations"""
#
#     def __init__(
#         self,
#         user_repository: AbstractRepository,
#         security_service: SecurityService,
#         admin_routes: str,
#     ) -> None:
#         """Init `AuthService` instance"""
#         self.user_repository = user_repository
#         self.security_service = security_service
#         self.ADMIN_ROUTES = admin_routes
#
#     async def login(
#         self,
#         form_data: OAuth2PasswordRequestForm,
#     ) -> Token:
#         """Check credentialds and return access token"""
#         user = await self._authenticate(form_data.username, form_data.password)
#         token = self.security_service.create_access_token(user.id)
#         return Token(
#             access_token=token,
#             token_type="bearer",
#         )
#
#     async def get_current_user(
#         self,
#         request: Request,
#         token: str,
#     ) -> User:
#         """Get user id from token and returns user instance"""
#         token_data = self.security_service.decode_token(token)
#         try:
#             user: User = await self.user_repository.get(item_id=token_data.sub)
#         except HTTPException as exc:
#             if exc.status_code == HTTP_404_NOT_FOUND:
#                 raise HTTPException(
#                     status_code=HTTP_401_UNAUTHORIZED,
#                     detail="You are not authenticated.",
#                 )
#             else:
#                 raise exc
#         if not user.is_active:
#             raise HTTPException(
#                 status_code=HTTP_401_UNAUTHORIZED,
#                 detail="You are not authenticated.",
#             )
#         self._check_permissions(request.url.path, user.role)
#         return user
#
#     async def _authenticate(self, login: str, password: str) -> User:
#         """Authenticate user"""
#         try:
#             user: User = await self.user_repository.get(
#                 item_id=login,
#                 item_id_field="login",
#             )
#         except HTTPException as exc:
#             if exc.status_code == HTTP_404_NOT_FOUND:
#                 raise HTTPException(
#                     status_code=HTTP_401_UNAUTHORIZED,
#                     detail="Invalid credentials.",
#                 )
#             else:
#                 raise exc
#         if not user.is_active:
#             raise HTTPException(
#                 status_code=HTTP_401_UNAUTHORIZED,
#                 detail="Invalid credentials.",
#             )
#         if not self.security_service.verify_password(password, user.password_hash):
#             raise HTTPException(
#                 status_code=HTTP_401_UNAUTHORIZED,
#                 detail="Invalid credentials.",
#             )
#         return user
#
#     def _check_permissions(
#         self,
#         url_path: str,
#         user_role: Role,
#     ) -> None:
#         """Check access permissions for endpoints"""
#         if re.match(self.ADMIN_ROUTES, url_path) and user_role < Role.ADMIN:
#             raise HTTPException(
#                 status_code=HTTP_403_FORBIDDEN,
#                 detail="You do not have access rights to perform this action.",
#             )
#
#     async def get_cloud_token(self) -> str:
#         """Return auth token for cloud service connection"""
#         data: dict = {
#             "username": settings.CLOUD_AUTH_LOGIN,
#             "password": settings.CLOUD_AUTH_PASS,
#         }
#         try:
#             bearer: dict = requests.post(url=settings.CLOUD_URL_AUTH, data=data).json()
#             token = bearer["access_token"]
#             return token
#         except Exception as e:
#             raise HTTPException(
#                 status_code=HTTP_400_BAD_REQUEST,
#                 detail=str(e),
#             )
#
#
# def get_auth_service(
#     user_repository: UserRepository = Depends(get_user_repository),
#     security_service: SecurityService = Depends(get_security_service),
# ) -> AuthService:
#     """Return `AuthService` for dependency injection"""
#     INFERENCES = r"^.*\/inferences\/delete"
#     CLINICS = r"^.*\/clinics.*"
#     USERS = r"^.*\/users(?!\/me\b).*"
#
#     ADMIN_ROUTES = "|".join([INFERENCES, CLINICS, USERS])
#     return AuthService(user_repository, security_service, ADMIN_ROUTES)
#
#
# async def get_current_user(
#     request: Request,
#     token: str = Depends(reusable_oauth2),
#     auth_service: AuthService = Depends(get_auth_service),
# ) -> User:
#     """Provides `get_current_user` of `AuthService` for dependency injection"""
#     return await auth_service.get_current_user(request, token)
