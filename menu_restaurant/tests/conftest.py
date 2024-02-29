import os

from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.util import deprecations

from menu_restaurant.database.dependency import get_db

# from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.session import Base

from ..main import app

load_dotenv('.env.work')

TEST_DATABASE_URL = os.getenv('DB_URL')

engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   autoflush=False,
                                   autocommit=False)

deprecations.SILENCE_UBER_WARNING = True


async def override_get_db():
    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            db.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.dependency_overrides[get_db] = override_get_db


client = AsyncClient(app)
# RedisCache.drob_all_cache()
