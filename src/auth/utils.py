from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from config import JWT_TOKEN
import jwt
from jwt import PyJWTError
from typing import Dict, Union
from auth.models import User
from database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        token = request.cookies.get("auth-token")
        try:
            jwt.decode(token, JWT_TOKEN, algorithms="HS256", audience=["fastapi-users:auth"])
            return True
        except PyJWTError as e:
            return False


def jwt_virefy_auth(request: Request) -> Dict:
    """Verify JWT Token from cookie
    :return if validation OK Dictionary like {"exception": False, "validation": True}
    if Error return {"exception": ErrorType, "validation": False}
    """
    token = request.cookies.get("auth-token")
    try:
        jwt.decode(token, JWT_TOKEN, algorithms="HS256", audience=["fastapi-users:auth"])
        return {"exception": False, "validation": True}
    except PyJWTError as e:
        return {"exception": e, "validation": False}
