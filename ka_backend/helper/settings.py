import sys

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret: str
    hostname: str
    sentry_url: str = ""


if "pytest" in sys.modules:
    settings = Settings(
        database_url="sqlite:///test.db",
        secret="TEST",
        hostname="http://localhost:3000",
    )
else:
    settings = Settings(".env")
