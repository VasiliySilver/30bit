"""
Базовый абстрактный репозиторий
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base

# Типы для Generic репозитория
ModelType = TypeVar("ModelType", bound=Base)
EntityType = TypeVar("EntityType")


class BaseRepository(ABC, Generic[ModelType, EntityType]):
    """
    Базовый абстрактный репозиторий с CRUD операциями
    
    Attributes:
        model: SQLAlchemy модель
        session: Асинхронная сессия базы данных
    """
    
    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория
        
        Args:
            session: Асинхронная сессия базы данных
        """
        self.session = session
    
    @property
    @abstractmethod
    def model(self) -> type[ModelType]:
        """Получить класс модели"""
        pass
    
    @abstractmethod
    async def to_entity(self, model: ModelType) -> EntityType:
        """
        Преобразовать модель в доменную сущность
        
        Args:
            model: SQLAlchemy модель
            
        Returns:
            EntityType: Доменная сущность
        """
        pass
    
    @abstractmethod
    async def to_model(self, entity: EntityType) -> ModelType:
        """
        Преобразовать доменную сущность в модель
        
        Args:
            entity: Доменная сущность
            
        Returns:
            ModelType: SQLAlchemy модель
        """
        pass
    
    async def get_by_id(self, id: int) -> Optional[EntityType]:
        """
        Получить сущность по ID
        
        Args:
            id: Идентификатор
            
        Returns:
            Optional[EntityType]: Доменная сущность или None
        """
        result = await self.session.get(self.model, id)
        if result is None:
            return None
        return await self.to_entity(result)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[EntityType]:
        """
        Получить все сущности с пагинацией
        
        Args:
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей
            
        Returns:
            List[EntityType]: Список доменных сущностей
        """
        from sqlalchemy import select
        
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [await self.to_entity(model) for model in models]
    
    async def create(self, entity: EntityType) -> EntityType:
        """
        Создать новую сущность
        
        Args:
            entity: Доменная сущность
            
        Returns:
            EntityType: Созданная доменная сущность с ID
        """
        model = await self.to_model(entity)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return await self.to_entity(model)
    
    async def update(self, entity: EntityType) -> EntityType:
        """
        Обновить существующую сущность
        
        Args:
            entity: Доменная сущность с ID
            
        Returns:
            EntityType: Обновленная доменная сущность
        """
        model = await self.to_model(entity)
        merged = await self.session.merge(model)
        await self.session.flush()
        await self.session.refresh(merged)
        return await self.to_entity(merged)
    
    async def delete(self, id: int) -> bool:
        """
        Удалить сущность по ID
        
        Args:
            id: Идентификатор
            
        Returns:
            bool: True если удалено, False если не найдено
        """
        model = await self.session.get(self.model, id)
        if model is None:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True