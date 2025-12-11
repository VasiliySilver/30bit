"""
SQLAlchemy модель для связи Item-Tag (Many-to-Many)
"""
from sqlalchemy import Table, Column, Integer, ForeignKey

from src.database import Base


# Таблица связи многие-ко-многим между Item и Tag
item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

__all__ = ["item_tags"]