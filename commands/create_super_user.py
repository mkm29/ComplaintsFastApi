import asyncclick as click

from db import database
from managers.user import UserManager
from models.enums import RoleType


@click.command()
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-w", "--password", type=str, required=True)
async def create_user(
    first_name: str, last_name: str, email: str, phone: str, iban: str, password: str
):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "iban": iban,
        "password": password,
        "role": RoleType.admin,
    }
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()


if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")
