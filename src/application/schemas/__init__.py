"""
Pydantic схемы для API
"""

from src.application.schemas.common import (
    PaginatedResponse,
    ErrorResponse,
    MessageResponse,
)
from src.application.schemas.user import UserCreate, UserUpdate, UserResponse
from src.application.schemas.tag import TagCreate, TagResponse
from src.application.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemFilterParams,
)

__all__ = [
    # Common
    "PaginatedResponse",
    "ErrorResponse",
    "MessageResponse",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Tag
    "TagCreate",
    "TagResponse",
    # Item
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
    "ItemFilterParams",
]
