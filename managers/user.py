import logging
from typing import Tuple

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext

from db import database
from managers.auth import AuthManager
from models import user
from models.enums import RoleType
from services.ses import SESService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ses_client = SESService()


class UserManager:
    @staticmethod
    async def register(user_data: dict) -> Tuple[dict, str]:
        user_data["password"] = pwd_context.hash(user_data["password"])
        # insert user into db
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        if not user_do:
            raise HTTPException(
                400, "There was an error saving the user to the database"
            )
        # send email
        try:
            response = ses_client.send_mail(
                [user_data["email"]],
                "Complaints System: New Registration",
                f"Welcome {user_data['first_name']} {user_data['last_name']}",
            )
        except Exception as exc:
            logging.error(exc)
            raise HTTPException(
                400, "There was an error sending the new registration email"
            )
        return user_do.__dict__, AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data: dict) -> Tuple[dict, str]:
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"])
        )
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong email or password")
        return dict(user_do), AuthManager.encode_token(user_do)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())

    @staticmethod
    async def get_user_by_email(email: str):
        return await database.fetch_all(user.select().where(user.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id: int):
        await database.execute(
            user.update().where(user.c.id == user_id).values(role=role)
        )
