"""
Настройка подключения к базе данных через SQLAlchemy
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.config import get_settings

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Движок базы данных
settings = get_settings()
engine: AsyncEngine = create_async_engine(
    settings.database_url, echo=settings.database_echo, future=True
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для получения сессии базы данных

    Yields:
        AsyncSession: Сессия базы данных
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Инициализация базы данных (создание таблиц)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """Удаление всех таблиц (для тестов)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
