import os
from os import environ

from dotenv import load_dotenv

load_dotenv("local.env")

EXAMPLE = environ.get("EXAMPLE_ENV_VARIABLE", "default")
DEBUG = environ.get("DEBUG", "False") == "True"

STAGE = environ.get("STAGE", "LOCAL")
if STAGE not in ("LOCAL", "TEST", "PRODUCTION"):
    raise ValueError


def get_database_url() -> str:
    return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        db=os.environ["POSTGRES_DB"],
    )
