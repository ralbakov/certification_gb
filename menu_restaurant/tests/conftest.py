import asyncio
import os

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.util import deprecations

from menu_restaurant.database.session import Base, get_db

from ..main import app

load_dotenv('.env.work')

deprecations.SILENCE_UBER_WARNING = True

TEST_DATABASE_URL = os.getenv('DB_URL_TEST')

engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

TestingSessionLocal = sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='session')
def event_loop():
    """Создает экземпляр стандартного цикла событий
    для каждого тестового случая."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
async def ac_client():
    async with AsyncClient(app=app, base_url='http://test') as ac_client:
        yield ac_client
