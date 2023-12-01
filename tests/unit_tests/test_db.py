import asyncio

from app.config import settings


@asyncio.coroutine
def test_init_db():
    assert settings.DB_NAME == "sdf"
