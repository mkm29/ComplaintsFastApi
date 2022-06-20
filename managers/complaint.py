from fastapi import HTTPException

from db import database
from models import complaint
from models.enums import RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        query = complaint.select()
        if user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user.id)
        if user["role"] == RoleType.approver:
            query = query.where(complaint.c.status == State.pending)
        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(complaint_data, user) -> object:
        complaint_data["complainer_id"] = user.id
        id_ = await database.execute(complaint.insert().values(**complaint_data))
        if not id_:
            raise HTTPException(400, "Error saving complain to database")
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id: int):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def update_state(complaint_id: int, state: State):
        await database.execute(
            complaint.update().where(complaint.c.id == complaint_id).values(state=state)
        )
