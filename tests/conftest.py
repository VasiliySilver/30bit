"""
Глобальные фикстуры для тестов
"""
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
from datetime import datetime

from src.database import Base
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.tag_repository import TagRepository
from src.infrastructure.repositories.item_repository import ItemRepository
from src.application.services.tag_service import TagService
from src.application.services.item_service import ItemService
from src.domain.entities.user import User


@pytest_asyncio.fixture
async def test_db():
    """Создает тестовую БД в памяти"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_user(test_db):
    """Создает тестового пользователя"""
    user_repo = UserRepository(test_db)
    user = User(
        id=None,
        email="test@example.com",
        display_name="Test User",
        created_at=datetime.now()
    )
    created_user = await user_repo.create(user)
    await test_db.commit()
    return created_user


@pytest_asyncio.fixture
async def tag_service(test_db):
    """Создает сервис тегов с тестовой БД"""
    return TagService(TagRepository(test_db))


@pytest_asyncio.fixture
async def item_service(test_db):
    """Создает сервис материалов с тестовой БД"""
    return ItemService(ItemRepository(test_db), TagRepository(test_db))