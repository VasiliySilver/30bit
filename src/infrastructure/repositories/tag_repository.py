"""
Репозиторий для работы с тегами
"""

from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.tag import Tag
from src.infrastructure.models.tag import TagModel
from src.infrastructure.repositories.base import BaseRepository


class TagRepository(BaseRepository[TagModel, Tag]):
    """
    Репозиторий для работы с тегами
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория тегов

        Args:
            session: Асинхронная сессия базы данных
        """
        super().__init__(session)

    @property
    def model(self) -> type[TagModel]:
        """Получить класс модели Tag"""
        return TagModel

    async def to_entity(self, model: TagModel) -> Tag:
        """
        Преобразовать модель в доменную сущность Tag

        Args:
            model: SQLAlchemy модель TagModel

        Returns:
            Tag: Доменная сущность тега
        """
        return Tag(id=model.id, user_id=model.user_id, name=model.name)

    async def to_model(self, entity: Tag) -> TagModel:
        """
        Преобразовать доменную сущность в модель TagModel

        Args:
            entity: Доменная сущность Tag

        Returns:
            TagModel: SQLAlchemy модель
        """
        return TagModel(id=entity.id, user_id=entity.user_id, name=entity.name)

    async def get_by_user_and_name(self, user_id: int, name: str) -> Optional[Tag]:
        """
        Получить тег пользователя по имени

        Args:
            user_id: ID пользователя
            name: Название тега

        Returns:
            Optional[Tag]: Доменная сущность тега или None
        """
        stmt = select(TagModel).where(
            and_(TagModel.user_id == user_id, TagModel.name == name.strip().lower())
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return await self.to_entity(model)

    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Tag]:
        """
        Получить все теги пользователя

        Args:
            user_id: ID пользователя
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей

        Returns:
            List[Tag]: Список доменных сущностей тегов
        """
        stmt = (
            select(TagModel)
            .where(TagModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [await self.to_entity(model) for model in models]

    async def exists_by_user_and_name(self, user_id: int, name: str) -> bool:
        """
        Проверить существование тега у пользователя

        Args:
            user_id: ID пользователя
            name: Название тега

        Returns:
            bool: True если тег существует
        """
        stmt = select(TagModel.id).where(
            and_(TagModel.user_id == user_id, TagModel.name == name.strip().lower())
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
