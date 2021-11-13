import sys

from pydantic import BaseSettings, DirectoryPath


class Settings(BaseSettings):
    database_url: str
    secret: str
    hostname: str
    frontend_url: str
    upload_path: DirectoryPath
    sentry_url: str = ""
    redis_url: str = ""


if "pytest" in sys.modules:
    settings = Settings(
        database_url="sqlite:///test.db",
        secret="TEST",
        hostname="http://localhost:3000",
        upload_path="./test/upload",
    )
else:
    settings = Settings(".env")
