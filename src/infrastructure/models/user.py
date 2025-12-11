"""
SQLAlchemy модель для User
"""

from typing import List
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserModel(Base):
    """
    Модель пользователя в базе данных

    Attributes:
        id: Первичный ключ
        email: Уникальная электронная почта
        display_name: Отображаемое имя
        created_at: Дата создания
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    # Связи
    items: Mapped[List["ItemModel"]] = relationship(
        "ItemModel", back_populates="user", cascade="all, delete-orphan"
    )
    tags: Mapped[List["TagModel"]] = relationship(
        "TagModel", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', display_name='{self.display_name}')>"
