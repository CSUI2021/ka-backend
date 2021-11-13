import asyncio
import json
import os

import pytest
from fastapi.testclient import TestClient

from ka_backend.app import app
from ka_backend.models import SIG, Competition, House, Story, Student


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True, scope="module")
@pytest.mark.asyncio
async def setup_db():
    import sqlalchemy

    from ka_backend.helper.database import metadata, settings

    engine = sqlalchemy.create_engine(settings.database_url)
    metadata.create_all(engine)

    HOUSES = [
        "Space",
        "Musical",
        "Historical",
        "Comedy",
        "Fantasy",
        "Mystery",
        "Superhero",
        "Action",
        "Animation",
        "Apocalypse",
        "Horror",
        "Romance",
    ]
    await House.objects.bulk_create(
        [House(nama=name, codename=name.lower()) for name in HOUSES]
    )

    with open("tests/data/users.json", "r") as f:
        await Student.objects.bulk_create([Student(**data) for data in json.load(f)])

    with open("tests/data/sig.json", "r") as f:
        await SIG.objects.bulk_create([SIG(**data) for data in json.load(f)])

    with open("tests/data/competitions.json", "r") as f:
        await Competition.objects.bulk_create(
            [Competition(**data) for data in json.load(f)]
        )

    with open("tests/data/stories.json", "r") as f:
        await Story.objects.bulk_create([Story(**data) for data in json.load(f)])

    yield
    metadata.drop_all(engine)
    os.remove("test.db")
