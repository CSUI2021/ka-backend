import databases
import ormar
import sqlalchemy

from ka_backend.helper.settings import settings

database = databases.Database(settings.database_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
