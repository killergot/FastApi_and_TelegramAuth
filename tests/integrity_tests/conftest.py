# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.api.depencies.db import get_db
from app.core.config import load_config

# Тестовая база данных (можно использовать SQLite для тестов)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_engine():
    """Создаем engine синхронно"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    conf = load_config()
    assert conf.MODE == "TEST"
    # Создаем таблицы
    async def setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.get_event_loop().run_until_complete(setup())
    return engine


@pytest.fixture
def test_session(test_engine):
    """Создаем сессию для тестов"""
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    # Создаем сессию асинхронно
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    session = loop.run_until_complete(async_session().__aenter__())

    yield session

    # Закрываем сессию
    loop.run_until_complete(session.close())


@pytest.fixture
def client(test_session):
    """Синхронный TestClient"""
    async def override_get_db():
        try:
            yield test_session
        finally:
            await test_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()