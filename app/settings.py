from typing import List
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_version: str
    description: str
    debug: bool
    database_name: str
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    jwt_secret_key: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    wise_api_key: str
    wise_url: str
    root_dir: str = os.path.dirname(os.path.abspath(__file__))
    tmp_dir: str = os.path.join(root_dir, "temp_files")
    charset: str = "UTF-8"
    from_email: str = "noreply@smigula.com"
    allowed_origins: List[str] = [
        "http://localhost",
        "https://localhost",
        "http://localhost:8080",
        "https://localhost:8080",
    ]
