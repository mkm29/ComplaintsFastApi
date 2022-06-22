from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)

# from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db import metadata

from .enums import State

complaint = Table(
    "complaints",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("title", String(120), nullable=False),
    Column("description", Text, nullable=False),
    Column("photo_url", String(200), nullable=False),
    Column("amount", Float, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("state", Enum(State), nullable=False, server_default=State.pending.name),
    Column("complainer_id", Integer, ForeignKey("users.id"), nullable=False),
)
