from dotenv import load_dotenv

from .settings import Settings

version = "0.4.1"
author = "Mitchell Murphy"

# this is not needed when deployed on K8s/ECS
load_dotenv()

settings = Settings()
