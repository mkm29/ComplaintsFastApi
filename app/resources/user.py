from typing import List, Optional

from fastapi import APIRouter, Depends
from starlette.requests import Request

from ..managers.auth import is_admin, oauth2_schema
from ..managers.user import UserManager
from ..models.enums import RoleType
from ..schemas.response.user import UserOut

router = APIRouter()


@router.get(
    "/users/",
    tags=["Users"],
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
    response_model=List[UserOut],
)
async def get_user_by_email(request: Request, email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    else:
        return await UserManager.get_all_users()


@router.put(
    "/users/{user_id}/make-admin",
    tags=["Users"],
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
)
async def update_role(request: Request, user_id: int):
    await UserManager.change_role(RoleType.admin, user_id)


@router.put(
    "/users/{user_id}/make-approver",
    tags=["Users"],
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
)
async def update_role_approver(request: Request, user_id: int):
    await UserManager.change_role(RoleType.approver, user_id)
