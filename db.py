from os import getenv

import databases
from dotenv import load_dotenv
from sqlalchemy import MetaData

# In Kubernetes this is not needed, env. vars will be attached to container
load_dotenv()


def get_url(as_dict: bool = False):
    params: dict = {
        "user": getenv("DB_USER"),
        "password": getenv("DB_PASS"),
        "host": getenv("DB_HOST"),
        "port": getenv("DB_PORT"),
        "database": getenv("DB_NAME"),
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


DATABASE_URL = get_url()
database = databases.Database(DATABASE_URL)
metadata = MetaData()
