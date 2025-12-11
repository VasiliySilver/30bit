"""
Конфигурация приложения через переменные окружения
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Настройки приложения
    
    Загружаются из переменных окружения или .env файла
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Настройки приложения
    app_name: str = "Reading List API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Настройки базы данных
    database_url: str = "sqlite+aiosqlite:///./reading_list.db"
    database_echo: bool = False
    
    # Настройки API
    api_prefix: str = "/api/v1"
    
    # Настройки пагинации
    default_limit: int = 20
    max_limit: int = 100


@lru_cache
def get_settings() -> Settings:
    """Получить настройки приложения (с кешированием)"""
    return Settings()