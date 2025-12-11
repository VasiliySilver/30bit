"""
Доменная сущность User
"""
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """
    Сущность пользователя
    
    Attributes:
        id: Уникальный идентификатор
        email: Электронная почта (уникальная)
        display_name: Отображаемое имя
        created_at: Дата создания
    """
    id: Optional[int]
    email: str
    display_name: str
    created_at: datetime
    
    def __post_init__(self):
        """Валидация после инициализации"""
        if not self.email or '@' not in self.email:
            raise ValueError("Email должен быть валидным")
        
        if not self.display_name or len(self.display_name.strip()) == 0:
            raise ValueError("Display name не может быть пустым")
        
        if self.created_at > datetime.now():
            raise ValueError("Дата создания не может быть в будущем")