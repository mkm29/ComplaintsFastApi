import logging
import os
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import update

from constants import TMP_DIR
from db import database
from models import complaint, user
from models.enums import RoleType, State
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo

s3 = None
ses = None
try:
    s3 = S3Service()
    ses = SESService()
except Exception as ex:
    logging.error(ex)


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
    async def create_complaint(complaint_data, user_) -> object:
        complaint_data["complainer_id"] = user_.id
        if not s3:
            raise HTTPException(400, "Error creating S3 client")
        # get encoded photo from data dictionary to write to disk (temporarily)
        encoded_photo = complaint_data.pop("encoded_photo")
        extension = complaint_data.pop("extension", None)
        # generate file name
        file_name = f"{uuid4()}.{extension}"
        path = os.path.join(TMP_DIR, file_name)
        decode_photo(path, encoded_photo)
        try:
            complaint_data["photo_url"] = s3.upload_file(
                file_path=path, extension=extension
            )
            # add S3 URL to data
            # complaint_data["photo_url"] = f"s3://{os.getenv('AWS_BUCKET_NAME')}/{file_name}"
        except Exception as exc:
            raise HTTPException(400, str(exc))
        id_ = await database.execute(complaint.insert().values(**complaint_data))
        # remove image from TMO_DIR
        try:
            os.remove(path)
        except OSError as exc:
            logging.error(exc)
        if not id_:
            raise HTTPException(400, "Error saving complain to database")
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id: int):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def update_state(complaint_id: int, state: State):
        _complaint = await database.fetch_one(
            complaint.select().where(complaint.c.id == complaint_id)
        )
        if not _complaint:
            raise HTTPException(400, "Complaint not found")
        _previous_status = _complaint.state
        # update complaint
        # update
        query = (
            update(complaint)
            .where(complaint.c.id == complaint_id)
            .values({"state": state})
        )
        await database.execute(query)
        # await database.execute(
        #     complaint.update().where(complaint.c.id == complaint_id).values(state=state)
        # )
        if ses:
            # need to find the user_id that is associated with this complaint -> complainer_id
            _user = await database.fetch_one(
                user.select().where(user.c.id == _complaint.complainer_id)
            )
            if _user:
                # need Python 3.10 to use match statement
                if state.value == "approved":
                    msg = "Congratulations your complaint has been approved! Check your bank account in 2 days."
                elif state.value == "rejected":
                    msg = "Sorry but your complaint has been denied."
                else:
                    msg = f"The status of your complaint has changed to {state.value}"
                response = ses.send_mail(
                    [_user.email],
                    "Complaint status changed",
                    msg,
                )
                logging.info(response)

    # could also set up a SQLAlchemy trigger, but do not want to duplicate the process
