from datetime import datetime, timedelta
from os import getenv
from typing import Optional

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from db import database
from models import user
from models.enums import RoleType

load_dotenv()


class AuthManager:
    @staticmethod
    def encode_token(user_data):
        try:
            payload = {
                "sub": user_data["id"],
                "exp": datetime.utcnow() + timedelta(minutes=15),
            }
            return jwt.encode(
                payload=payload, key=getenv("JWT_SECRET_KEY"), algorithm="HS256"
            )
        except Exception as ex:
            # log exception
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(
                res.credentials, getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            request.state.user = user_data
            return payload
        except jwt.ExpiredSignatureError:
            # refresh?
            raise HTTPException(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


oauth2_schema = CustomHTTPBearer()


def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")
