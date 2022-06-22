from typing import Optional, Union

from fastapi import APIRouter

from ..managers.user import UserManager
from ..schemas.request.user import LoginUserIn, RegisterUserIn

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: RegisterUserIn) -> Optional[Union[dict, str]]:
    user, token = await UserManager.register(user_data.dict())
    del user["password"]
    return {"user": user, "token": token}


@router.post("/login/")
async def login(user_data: LoginUserIn) -> Optional[Union[dict, str]]:
    user, token = await UserManager.login(user_data.dict())
    del user["password"]
    return {"user": user, "token": token}
