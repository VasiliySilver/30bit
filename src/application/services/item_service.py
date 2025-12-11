"""
Сервис для работы с материалами (Item)
"""

from typing import List, Optional
from datetime import datetime

from src.domain.entities.item import Item
from src.domain.enums import ItemKind, ItemStatus, Priority
from src.domain.exceptions import EntityNotFoundError, PermissionDeniedError
from src.infrastructure.repositories.item_repository import ItemRepository
from src.infrastructure.repositories.tag_repository import TagRepository
from src.application.schemas.item import ItemCreate, ItemUpdate, ItemResponse


class ItemService:
    """
    Сервис для бизнес-логики работы с материалами
    """

    def __init__(self, item_repository: ItemRepository, tag_repository: TagRepository):
        """
        Инициализация сервиса

        Args:
            item_repository: Репозиторий материалов
            tag_repository: Репозиторий тегов
        """
        self.item_repository = item_repository
        self.tag_repository = tag_repository

    async def create_item(self, user_id: int, data: ItemCreate) -> ItemResponse:
        """
        Создать новый материал

        Args:
            user_id: ID пользователя-владельца
            data: Данные для создания материала

        Returns:
            ItemResponse: Созданный материал
        """
        # Создаем доменную сущность
        now = datetime.now()
        entity = Item(
            id=None,
            user_id=user_id,
            title=data.title,
            kind=data.kind,
            status=data.status,
            priority=data.priority,
            notes=data.notes,
            created_at=now,
            updated_at=now,
        )

        # Сохраняем в БД
        created_entity = await self.item_repository.create(entity)

        # Добавляем теги, если указаны
        if data.tag_ids:
            # Проверяем, что все теги принадлежат пользователю
            await self._validate_tags_ownership(user_id, data.tag_ids)
            await self.item_repository.add_tags(created_entity.id, data.tag_ids)

        # Возвращаем ответ
        return ItemResponse(
            id=created_entity.id,
            user_id=created_entity.user_id,
            title=created_entity.title,
            kind=created_entity.kind,
            status=created_entity.status,
            priority=created_entity.priority,
            notes=created_entity.notes,
            created_at=created_entity.created_at,
            updated_at=created_entity.updated_at,
            tag_ids=data.tag_ids,
        )

    async def get_item(self, item_id: int, user_id: int) -> ItemResponse:
        """
        Получить материал по ID

        Args:
            item_id: ID материала
            user_id: ID пользователя (для проверки доступа)

        Returns:
            ItemResponse: Данные материала

        Raises:
            EntityNotFoundError: Если материал не найден
            PermissionDeniedError: Если материал не принадлежит пользователю
        """
        result = await self.item_repository.get_by_id_with_tags(item_id)

        if result is None:
            raise EntityNotFoundError("Item", item_id)

        entity, tag_ids = result

        # Проверяем, что материал принадлежит пользователю
        if entity.user_id != user_id:
            raise PermissionDeniedError("Доступ к материалу запрещен")

        return ItemResponse(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            kind=entity.kind,
            status=entity.status,
            priority=entity.priority,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            tag_ids=tag_ids,
        )

    async def get_user_items(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        kind: Optional[ItemKind] = None,
        status: Optional[ItemStatus] = None,
        priority: Optional[Priority] = None,
    ) -> List[ItemResponse]:
        """
        Получить список материалов пользователя с фильтрацией

        Args:
            user_id: ID пользователя
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей
            kind: Фильтр по типу материала
            status: Фильтр по статусу
            priority: Фильтр по приоритету

        Returns:
            List[ItemResponse]: Список материалов
        """
        entities = await self.item_repository.get_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            kind=kind,
            status=status,
            priority=priority,
        )

        # Преобразуем в ответы
        result = []
        for entity in entities:
            # Получаем теги для каждого материала
            item_with_tags = await self.item_repository.get_by_id_with_tags(entity.id)
            if item_with_tags:
                _, tag_ids = item_with_tags
            else:
                tag_ids = []

            result.append(
                ItemResponse(
                    id=entity.id,
                    user_id=entity.user_id,
                    title=entity.title,
                    kind=entity.kind,
                    status=entity.status,
                    priority=entity.priority,
                    notes=entity.notes,
                    created_at=entity.created_at,
                    updated_at=entity.updated_at,
                    tag_ids=tag_ids,
                )
            )

        return result

    async def update_item(
        self, item_id: int, user_id: int, data: ItemUpdate
    ) -> ItemResponse:
        """
        Обновить материал

        Args:
            item_id: ID материала
            user_id: ID пользователя (для проверки доступа)
            data: Данные для обновления

        Returns:
            ItemResponse: Обновленный материал

        Raises:
            EntityNotFoundError: Если материал не найден
            PermissionDeniedError: Если материал не принадлежит пользователю
        """
        # Получаем существующий материал
        entity = await self.item_repository.get_by_id(item_id)

        if entity is None:
            raise EntityNotFoundError("Item", item_id)

        # Проверяем, что материал принадлежит пользователю
        if entity.user_id != user_id:
            raise PermissionDeniedError("Доступ к материалу запрещен")

        # Обновляем поля доменной сущности
        entity.update(
            title=data.title,
            kind=data.kind,
            status=data.status,
            priority=data.priority,
            notes=data.notes,
        )

        # Сохраняем в БД
        updated_entity = await self.item_repository.update(entity)

        # Обновляем теги, если указаны
        if data.tag_ids is not None:
            # Проверяем, что все теги принадлежат пользователю
            await self._validate_tags_ownership(user_id, data.tag_ids)
            await self.item_repository.set_tags(item_id, data.tag_ids)

        # Получаем актуальные теги
        result = await self.item_repository.get_by_id_with_tags(item_id)
        tag_ids = result[1] if result else []

        return ItemResponse(
            id=updated_entity.id,
            user_id=updated_entity.user_id,
            title=updated_entity.title,
            kind=updated_entity.kind,
            status=updated_entity.status,
            priority=updated_entity.priority,
            notes=updated_entity.notes,
            created_at=updated_entity.created_at,
            updated_at=updated_entity.updated_at,
            tag_ids=tag_ids,
        )

    async def delete_item(self, item_id: int, user_id: int) -> bool:
        """
        Удалить материал

        Args:
            item_id: ID материала
            user_id: ID пользователя (для проверки доступа)

        Returns:
            bool: True если удалено

        Raises:
            EntityNotFoundError: Если материал не найден
            PermissionDeniedError: Если материал не принадлежит пользователю
        """
        # Получаем существующий материал
        entity = await self.item_repository.get_by_id(item_id)

        if entity is None:
            raise EntityNotFoundError("Item", item_id)

        # Проверяем, что материал принадлежит пользователю
        if entity.user_id != user_id:
            raise PermissionDeniedError("Доступ к материалу запрещен")

        # Удаляем
        return await self.item_repository.delete(item_id)

    async def _validate_tags_ownership(self, user_id: int, tag_ids: List[int]) -> None:
        """
        Проверить, что все теги принадлежат пользователю

        Args:
            user_id: ID пользователя
            tag_ids: Список ID тегов

        Raises:
            PermissionDeniedError: Если хотя бы один тег не принадлежит пользователю
        """
        for tag_id in tag_ids:
            tag = await self.tag_repository.get_by_id(tag_id)
            if tag is None or tag.user_id != user_id:
                raise PermissionDeniedError(
                    f"Тег с id={tag_id} не принадлежит пользователю"
                )
