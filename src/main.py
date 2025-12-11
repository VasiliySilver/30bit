"""
Главный файл FastAPI приложения
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import items_router, tags_router, user_router
from src.config import get_settings
from src.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения

    При старте: инициализация БД
    При остановке: очистка ресурсов
    """
    # Инициализация БД при старте
    await init_db()
    yield
    # Очистка при остановке (если нужно)


# Создание приложения FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(user_router, prefix=settings.api_prefix)
app.include_router(items_router, prefix=settings.api_prefix)
app.include_router(tags_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """
    Корневой эндпоинт
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """
    Проверка здоровья приложения
    """
    return {"status": "healthy"}
