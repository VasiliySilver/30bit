"""
API роутеры
"""

from src.api.routers.users import router as user_router
from src.api.routers.items import router as items_router
from src.api.routers.tags import router as tags_router


__all__ = ["user_router", "items_router", "tags_router"]
