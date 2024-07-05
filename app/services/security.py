# from datetime import datetime, timedelta
# from typing import Any
#
# from fastapi import HTTPException
# from jose import jwt
# from passlib.context import CryptContext
# from pydantic import ValidationError
# from starlette.status import HTTP_403_FORBIDDEN
#
#
#
# from app.core.security import pwd_context
#
#
# class SecurityService:
#     """Service class which provides security operations"""
#
#     def __init__(
#         self,
#         pwd_context: CryptContext,
#         secret_key: str,
#         access_token_algorythm: str,
#         expires: int,
#     ) -> None:
#         """Init `SecurityService` instance"""
#         self.pwd_context = pwd_context
#         self.SECRET_KEY = secret_key
#         self.ACCESS_TOKEN_ALGORITHM = access_token_algorythm
#         self.EXPIRES_DELTA = timedelta(expires)
#
#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         """Compare password with hashed password"""
#         return self.pwd_context.verify(plain_password, hashed_password)
#
#     def get_password_hash(self, password: str) -> str:
#         """Hash password"""
#         return self.pwd_context.hash(password)
#
#     def create_access_token(
#         self,
#         subject: str | Any,
#     ) -> str:
#         """Create access token"""
#         expire = datetime.utcnow() + self.EXPIRES_DELTA
#         to_encode = {'exp': expire, 'sub': str(subject)}
#         encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, self.ACCESS_TOKEN_ALGORITHM)
#         return encoded_jwt
#
#     def decode_token(self, token: str) -> TokenPayload:
#         """Decode token and return payload."""
#         try:
#             payload = jwt.decode(token, self.SECRET_KEY, self.ACCESS_TOKEN_ALGORITHM)
#             return TokenPayload(**payload)
#         except Exception as e:
#             print(e)
#             raise HTTPException(
#                 status_code=HTTP_403_FORBIDDEN,
#                 detail='Could not validate credentials.',
#             )
#
#
# def get_security_service() -> SecurityService:
#     """Return `SecurityService` instance for dependency injection"""
#     return SecurityService(
#         pwd_context=pwd_context,
#         secret_key=settings.SECRET_KEY,
#         access_token_algorythm=settings.ACCESS_TOKEN_ALGORITHM,
#         expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
#     )
