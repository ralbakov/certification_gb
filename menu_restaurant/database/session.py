import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import deprecations

load_dotenv('.env.work')

deprecations.SILENCE_UBER_WARNING = True

SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

AsyncSessionLocal = sessionmaker(bind=engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
