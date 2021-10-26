import sys
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret: str
    hostname: str


if "pytest" in sys.modules:
    settings = Settings(
        database_url="sqlite://:memory:",
        secret="TEST",
        hostname="http://localhost:3000",
    )
else:
    settings = Settings(".env")
