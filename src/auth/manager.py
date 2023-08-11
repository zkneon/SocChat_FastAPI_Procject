from typing import Optional, Union, Any
import aiohttp
import asyncio
import requests
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, InvalidPasswordException, models
from fastapi_users import exceptions
from pydantic import EmailStr
from fastapi.responses import RedirectResponse

from auth.models import User
from auth.schemas import UserCreate
from config import JWT_TOKEN, HUNT_API_KEY
from auth.utils import get_user_db

SECRET = JWT_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
        else:
            """Validate email with API https://hunter.io/verify add token from it to .env"""
            await self.validation_email(user_create.email)

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)

        return created_user

    async def validation_email(self, email: EmailStr):

        async with aiohttp.ClientSession() as session:
            url = 'https://api.hunter.io/v2/email-verifier'
            async with session.get(url, params={'email': email, 'api_key': HUNT_API_KEY}) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    if r["data"]["status"] == "invalid":
                        raise HTTPException(
                            status_code=400,
                            detail=[{"msg": "Email address is invalid. Please check It. And try again!"}]
                        )

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
