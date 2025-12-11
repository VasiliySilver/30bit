"""
SQLAlchemy модель для Tag
"""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class TagModel(Base):
    """
    Модель тега в базе данных

    Attributes:
        id: Первичный ключ
        user_id: Внешний ключ на пользователя
        name: Название тега (уникально в рамках пользователя)
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Уникальность: тег должен быть уникальным в рамках одного пользователя
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_tag"),)

    # Связи
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="tags")
    items: Mapped[list["ItemModel"]] = relationship(
        "ItemModel", secondary="item_tags", back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, user_id={self.user_id}, name='{self.name}')>"
