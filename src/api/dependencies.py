"""
Зависимости для FastAPI (Dependency Injection)
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.tag_repository import TagRepository
from src.infrastructure.repositories.item_repository import ItemRepository
from src.application.services.item_service import ItemService
from src.application.services.tag_service import TagService


async def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    """
    Получить репозиторий пользователей
    
    Args:
        db: Сессия базы данных
        
    Returns:
        UserRepository: Репозиторий пользователей
    """
    return UserRepository(db)


async def get_tag_repository(
    db: AsyncSession = Depends(get_db)
) -> TagRepository:
    """
    Получить репозиторий тегов
    
    Args:
        db: Сессия базы данных
        
    Returns:
        TagRepository: Репозиторий тегов
    """
    return TagRepository(db)


async def get_item_repository(
    db: AsyncSession = Depends(get_db)
) -> ItemRepository:
    """
    Получить репозиторий материалов
    
    Args:
        db: Сессия базы данных
        
    Returns:
        ItemRepository: Репозиторий материалов
    """
    return ItemRepository(db)


async def get_tag_service(
    tag_repository: TagRepository = Depends(get_tag_repository)
) -> TagService:
    """
    Получить сервис тегов
    
    Args:
        tag_repository: Репозиторий тегов
        
    Returns:
        TagService: Сервис тегов
    """
    return TagService(tag_repository)


async def get_item_service(
    item_repository: ItemRepository = Depends(get_item_repository),
    tag_repository: TagRepository = Depends(get_tag_repository)
) -> ItemService:
    """
    Получить сервис материалов
    
    Args:
        item_repository: Репозиторий материалов
        tag_repository: Репозиторий тегов
        
    Returns:
        ItemService: Сервис материалов
    """
    return ItemService(item_repository, tag_repository)


# Временная функция для получения текущего пользователя
# TODO: Заменить на реальную аутентификацию
async def get_current_user_id() -> int:
    """
    Получить ID текущего пользователя
    
    Временная заглушка, всегда возвращает user_id=1
    В реальном приложении здесь должна быть JWT аутентификация
    
    Returns:
        int: ID пользователя
    """
    return 1