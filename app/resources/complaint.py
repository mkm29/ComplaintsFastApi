from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from ..managers.auth import is_admin, is_approver, is_complainer, oauth2_schema
from ..managers.complaint import ComplaintManager
from ..models.enums import State
from ..schemas.request.complaint import ComplaintIn
from ..schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


@router.get(
    "/complaints/",
    dependencies=[Depends(oauth2_schema)],
    response_model=List[ComplaintOut],
)
async def get_complaints(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(400, "User does not exist in state")
    return await ComplaintManager.get_complaints(user)


@router.post(
    "/complaints/",
    dependencies=[Depends(oauth2_schema), Depends(is_complainer)],
    status_code=201,
)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete(
    "/complaints/{complaint_id}",
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
)
async def delete_complaint(complaint_id: int):
    try:
        await ComplaintManager.delete(complaint_id)
    except Exception as ex:
        return {"errors": ex}
    return {"message": "Complaint was successfully deleted"}


@router.put(
    "/complaints/{complaint_id}/{to_state}",
    dependencies=[Depends(oauth2_schema), Depends(is_approver)],
    status_code=204,
)
async def update_state(complaint_id: int, to_state: State):
    await ComplaintManager.update_state(complaint_id, to_state)
