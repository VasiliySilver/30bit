"""
Глобальные фикстуры для тестов
"""

import os
from datetime import datetime
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.database import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.api.routers import items_router, tags_router, user_router
from src.api.dependencies import get_current_user_id
from src.domain.entities.user import User
from src.application.services.item_service import ItemService
from src.application.services.tag_service import TagService
from src.infrastructure.repositories.item_repository import ItemRepository
from src.infrastructure.repositories.tag_repository import TagRepository

settings = get_settings()

# Создание тестового приложения без lifespan
test_app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# Настройка CORS для тестового приложения
test_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров к тестовому приложению
test_app.include_router(user_router, prefix=settings.api_prefix)
test_app.include_router(items_router, prefix=settings.api_prefix)
test_app.include_router(tags_router, prefix=settings.api_prefix)


if os.path.exists("test.db"):
    os.remove("test.db")
engine = create_async_engine(
    "sqlite+aiosqlite:///test.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest_asyncio.fixture
async def setup_db():
    # Создаём таблицы единожды за сессию
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Не dispose, так как function scope


@pytest_asyncio.fixture
async def client(setup_db):
    # Патчим зависимость get_db чтобы приложение использовало наш in-memory engine
    try:
        from src.database import get_db as _dep_to_override
    except Exception:
        _dep_to_override = None

    async def _override_db_session():
        async with AsyncSession(engine, expire_on_commit=False) as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def _override_get_current_user_id():
        return 1  # Для тестов всегда возвращаем user_id=1

    if _dep_to_override is not None:
        test_app.dependency_overrides[_dep_to_override] = _override_db_session
        test_app.dependency_overrides[get_current_user_id] = (
            _override_get_current_user_id
        )

    # Создаем тестового пользователя в базе
    async with AsyncSession(engine, expire_on_commit=False) as session:
        from src.infrastructure.repositories.user_repository import UserRepository

        user_repo = UserRepository(session)
        test_user = User(
            id=1,
            email="test@example.com",
            display_name="Test User",
            created_at=datetime.now(),
        )
        await user_repo.create(test_user)
        await session.commit()

    with TestClient(test_app) as test_client:
        yield test_client

    test_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user():
    """Фикстура для тестового пользователя"""
    return User(
        id=1,
        email="test@example.com",
        display_name="Test User",
        created_at=datetime.now(),
    )


@pytest_asyncio.fixture
async def item_service(setup_db):
    """Фикстура для ItemService"""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        item_repo = ItemRepository(session)
        tag_repo = TagRepository(session)
        service = ItemService(item_repo, tag_repo)
        yield service


@pytest_asyncio.fixture
async def tag_service(setup_db):
    """Фикстура для TagService"""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        repo = TagRepository(session)
        service = TagService(repo)
        yield service
