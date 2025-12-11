"""
SQLAlchemy модель для Item
"""

from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.domain.enums import ItemKind, ItemStatus, Priority


if TYPE_CHECKING:
    from src.infrastructure.models.user import UserModel
    from src.infrastructure.models.tag import TagModel


class ItemModel(Base):
    """
    Модель материала (книга/статья) в базе данных

    Attributes:
        id: Первичный ключ
        user_id: Внешний ключ на пользователя
        title: Название материала
        kind: Тип материала (book|article)
        status: Статус прочтения (planned|reading|done)
        priority: Приоритет (low|normal|high)
        notes: Заметки
        created_at: Дата создания
        updated_at: Дата обновления
    """

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    kind: Mapped[ItemKind] = mapped_column(
        SQLEnum(ItemKind, native_enum=False), nullable=False, index=True
    )
    status: Mapped[ItemStatus] = mapped_column(
        SQLEnum(ItemStatus, native_enum=False), nullable=False, index=True
    )
    priority: Mapped[Priority] = mapped_column(
        SQLEnum(Priority, native_enum=False), nullable=False, index=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Связи
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="items")
    tags: Mapped[list["TagModel"]] = relationship(
        "TagModel", secondary="item_tags", back_populates="items"
    )

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, user_id={self.user_id}, title='{self.title}', status={self.status})>"
