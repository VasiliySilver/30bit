"""
Репозиторий для работы с материалами (Item)
"""
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.item import Item
from src.domain.enums import ItemKind, ItemStatus, Priority
from src.infrastructure.models.item import ItemModel
from src.infrastructure.models.tag import TagModel
from src.infrastructure.repositories.base import BaseRepository


class ItemRepository(BaseRepository[ItemModel, Item]):
    """
    Репозиторий для работы с материалами
    """
    
    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория материалов
        
        Args:
            session: Асинхронная сессия базы данных
        """
        super().__init__(session)
    
    @property
    def model(self) -> type[ItemModel]:
        """Получить класс модели Item"""
        return ItemModel
    
    async def to_entity(self, model: ItemModel) -> Item:
        """
        Преобразовать модель в доменную сущность Item
        
        Args:
            model: SQLAlchemy модель ItemModel
            
        Returns:
            Item: Доменная сущность материала
        """
        return Item(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            kind=model.kind,
            status=model.status,
            priority=model.priority,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    async def to_model(self, entity: Item) -> ItemModel:
        """
        Преобразовать доменную сущность в модель ItemModel
        
        Args:
            entity: Доменная сущность Item
            
        Returns:
            ItemModel: SQLAlchemy модель
        """
        return ItemModel(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            kind=entity.kind,
            status=entity.status,
            priority=entity.priority,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    async def get_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        kind: Optional[ItemKind] = None,
        status: Optional[ItemStatus] = None,
        priority: Optional[Priority] = None
    ) -> List[Item]:
        """
        Получить материалы пользователя с фильтрацией
        
        Args:
            user_id: ID пользователя
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей
            kind: Фильтр по типу материала
            status: Фильтр по статусу
            priority: Фильтр по приоритету
            
        Returns:
            List[Item]: Список доменных сущностей материалов
        """
        conditions = [ItemModel.user_id == user_id]
        
        if kind is not None:
            conditions.append(ItemModel.kind == kind)
        
        if status is not None:
            conditions.append(ItemModel.status == status)
        
        if priority is not None:
            conditions.append(ItemModel.priority == priority)
        
        stmt = select(ItemModel).where(
            and_(*conditions)
        ).offset(skip).limit(limit).order_by(ItemModel.created_at.desc())
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [await self.to_entity(model) for model in models]
    
    async def get_by_id_with_tags(self, item_id: int) -> Optional[tuple[Item, List[int]]]:
        """
        Получить материал с ID его тегов
        
        Args:
            item_id: ID материала
            
        Returns:
            Optional[tuple[Item, List[int]]]: Кортеж (материал, список ID тегов) или None
        """
        stmt = select(ItemModel).where(
            ItemModel.id == item_id
        ).options(selectinload(ItemModel.tags))
        
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        entity = await self.to_entity(model)
        tag_ids = [tag.id for tag in model.tags]
        
        return entity, tag_ids
    
    async def add_tags(self, item_id: int, tag_ids: List[int]) -> None:
        """
        Добавить теги к материалу
        
        Args:
            item_id: ID материала
            tag_ids: Список ID тегов
        """
        item = await self.session.get(ItemModel, item_id)
        if item is None:
            return
        
        # Получаем теги по ID
        stmt = select(TagModel).where(TagModel.id.in_(tag_ids))
        result = await self.session.execute(stmt)
        tags = result.scalars().all()
        
        # Добавляем теги к материалу
        for tag in tags:
            if tag not in item.tags:
                item.tags.append(tag)
        
        await self.session.flush()
    
    async def remove_tags(self, item_id: int, tag_ids: List[int]) -> None:
        """
        Удалить теги у материала
        
        Args:
            item_id: ID материала
            tag_ids: Список ID тегов для удаления
        """
        item = await self.session.get(ItemModel, item_id, options=[selectinload(ItemModel.tags)])
        if item is None:
            return
        
        # Удаляем теги
        item.tags = [tag for tag in item.tags if tag.id not in tag_ids]
        
        await self.session.flush()
    
    async def set_tags(self, item_id: int, tag_ids: List[int]) -> None:
        """
        Установить теги материала (заменить все существующие)
        
        Args:
            item_id: ID материала
            tag_ids: Список ID тегов
        """
        item = await self.session.get(ItemModel, item_id, options=[selectinload(ItemModel.tags)])
        if item is None:
            return
        
        # Получаем новые теги
        stmt = select(TagModel).where(TagModel.id.in_(tag_ids))
        result = await self.session.execute(stmt)
        tags = result.scalars().all()
        
        # Заменяем теги
        item.tags = list(tags)
        
        await self.session.flush()