from datetime import datetime

from pydantic import BaseModel

from ...models.enums import State

from ..base import BaseComplaint


class ComplaintOut(BaseComplaint):
    id: int
    created_at: datetime
    photo_url: str
    state: State
