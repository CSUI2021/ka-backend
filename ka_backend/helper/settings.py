from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret: str


settings = Settings(".env")
