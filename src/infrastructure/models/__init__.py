"""
SQLAlchemy модели для Reading List API
"""

from src.infrastructure.models.user import UserModel
from src.infrastructure.models.tag import TagModel
from src.infrastructure.models.item import ItemModel
# Импортируем таблицу напрямую из модуля
import src.infrastructure.models.item_tag

__all__ = [
    "UserModel",
    "TagModel",
    "ItemModel",
]
