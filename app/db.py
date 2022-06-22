import databases
from sqlalchemy import MetaData

from . import settings


def get_database_url(as_dict: bool = False):
    params: dict = {
        "user": settings.database_user,
        "password": settings.database_password,
        "host": settings.database_host,
        "port": settings.database_port,
        "database": settings.database_name,
    }
    if as_dict:
        return params
    return "postgresql+psycopg2://%s:%s@%s:%d/%s" % (
        params["user"],
        params["password"],
        params["host"],
        int(params["port"]),
        params["database"],
    )


database = databases.Database(get_database_url())
metadata = MetaData()
