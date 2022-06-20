from sqlalchemy import Column, Enum, Integer, String, Table

from db import metadata

from .enums import RoleType

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("email", String(120), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column(
        "role", Enum(RoleType), nullable=False, server_default=RoleType.complainer.name
    ),
    Column("phone", String(20)),
    Column("iban", String(200)),
)
