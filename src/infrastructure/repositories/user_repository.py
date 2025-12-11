"""
Репозиторий для работы с пользователями
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.infrastructure.models.user import UserModel
from src.infrastructure.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel, User]):
    """
    Репозиторий для работы с пользователями
    """
    
    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория пользователей
        
        Args:
            session: Асинхронная сессия базы данных
        """
        super().__init__(session)
    
    @property
    def model(self) -> type[UserModel]:
        """Получить класс модели User"""
        return UserModel
    
    async def to_entity(self, model: UserModel) -> User:
        """
        Преобразовать модель в доменную сущность User
        
        Args:
            model: SQLAlchemy модель UserModel
            
        Returns:
            User: Доменная сущность пользователя
        """
        return User(
            id=model.id,
            email=model.email,
            display_name=model.display_name,
            created_at=model.created_at
        )
    
    async def to_model(self, entity: User) -> UserModel:
        """
        Преобразовать доменную сущность в модель UserModel
        
        Args:
            entity: Доменная сущность User
            
        Returns:
            UserModel: SQLAlchemy модель
        """
        return UserModel(
            id=entity.id,
            email=entity.email,
            display_name=entity.display_name,
            created_at=entity.created_at
        )
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Получить пользователя по email
        
        Args:
            email: Email пользователя
            
        Returns:
            Optional[User]: Доменная сущность пользователя или None
        """
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return await self.to_entity(model)
    
    async def exists_by_email(self, email: str) -> bool:
        """
        Проверить существование пользователя по email
        
        Args:
            email: Email пользователя
            
        Returns:
            bool: True если пользователь существует
        """
        stmt = select(UserModel.id).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None