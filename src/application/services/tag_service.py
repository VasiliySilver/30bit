"""
Сервис для работы с тегами
"""
from typing import List

from src.domain.entities.tag import Tag
from src.domain.exceptions import EntityNotFoundError, DuplicateEntityError, PermissionDeniedError
from src.infrastructure.repositories.tag_repository import TagRepository
from src.application.schemas.tag import TagCreate, TagResponse


class TagService:
    """
    Сервис для бизнес-логики работы с тегами
    """
    
    def __init__(self, tag_repository: TagRepository):
        """
        Инициализация сервиса
        
        Args:
            tag_repository: Репозиторий тегов
        """
        self.tag_repository = tag_repository
    
    async def create_tag(self, user_id: int, data: TagCreate) -> TagResponse:
        """
        Создать новый тег
        
        Args:
            user_id: ID пользователя-владельца
            data: Данные для создания тега
            
        Returns:
            TagResponse: Созданный тег
            
        Raises:
            DuplicateEntityError: Если тег с таким именем уже существует у пользователя
        """
        # Проверяем, что тег с таким именем не существует у пользователя
        existing = await self.tag_repository.get_by_user_and_name(user_id, data.name)
        if existing is not None:
            raise DuplicateEntityError("Tag", "name", data.name)
        
        # Создаем доменную сущность
        entity = Tag(
            id=None,
            user_id=user_id,
            name=data.name
        )
        
        # Сохраняем в БД
        created_entity = await self.tag_repository.create(entity)
        
        return TagResponse(
            id=created_entity.id,
            user_id=created_entity.user_id,
            name=created_entity.name
        )
    
    async def get_tag(self, tag_id: int, user_id: int) -> TagResponse:
        """
        Получить тег по ID
        
        Args:
            tag_id: ID тега
            user_id: ID пользователя (для проверки доступа)
            
        Returns:
            TagResponse: Данные тега
            
        Raises:
            EntityNotFoundError: Если тег не найден
            PermissionDeniedError: Если тег не принадлежит пользователю
        """
        entity = await self.tag_repository.get_by_id(tag_id)
        
        if entity is None:
            raise EntityNotFoundError("Tag", tag_id)
        
        # Проверяем, что тег принадлежит пользователю
        if entity.user_id != user_id:
            raise PermissionDeniedError("Доступ к тегу запрещен")
        
        return TagResponse(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name
        )
    
    async def get_user_tags(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TagResponse]:
        """
        Получить список тегов пользователя
        
        Args:
            user_id: ID пользователя
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей
            
        Returns:
            List[TagResponse]: Список тегов
        """
        entities = await self.tag_repository.get_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit
        )
        
        return [
            TagResponse(
                id=entity.id,
                user_id=entity.user_id,
                name=entity.name
            )
            for entity in entities
        ]
    
    async def delete_tag(self, tag_id: int, user_id: int) -> bool:
        """
        Удалить тег
        
        Args:
            tag_id: ID тега
            user_id: ID пользователя (для проверки доступа)
            
        Returns:
            bool: True если удалено
            
        Raises:
            EntityNotFoundError: Если тег не найден
            PermissionDeniedError: Если тег не принадлежит пользователю
        """
        # Получаем существующий тег
        entity = await self.tag_repository.get_by_id(tag_id)
        
        if entity is None:
            raise EntityNotFoundError("Tag", tag_id)
        
        # Проверяем, что тег принадлежит пользователю
        if entity.user_id != user_id:
            raise PermissionDeniedError("Доступ к тегу запрещен")
        
        # Удаляем (связи с материалами удалятся автоматически через каскад)
        return await self.tag_repository.delete(tag_id)