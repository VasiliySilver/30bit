"""
Доменная сущность Tag
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Tag:
    """
    Сущность тега
    
    Attributes:
        id: Уникальный идентификатор
        user_id: ID пользователя-владельца
        name: Название тега (уникально в рамках пользователя)
    """
    id: Optional[int]
    user_id: int
    name: str
    
    def __post_init__(self):
        """Валидация после инициализации"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Название тега не может быть пустым")
        
        if self.user_id <= 0:
            raise ValueError("User ID должен быть положительным числом")
        
        # Нормализуем название тега (убираем лишние пробелы, приводим к нижнему регистру)
        self.name = self.name.strip().lower()
        
        if len(self.name) > 50:
            raise ValueError("Название тега не может быть длиннее 50 символов")