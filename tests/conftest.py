import asyncio

import pytest

from app.config import settings
from app.dataaccess.database import Base, engine
from app.dataaccess.models import *


@asyncio.coroutine
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert settings.MODE == "TEST"
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
