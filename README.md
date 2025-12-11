# 📚 Reading List API

Мини‑сервис для ведения списка книг и статей с метками и статусами.  
Стек: **Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Docker**

---

## 🚀 Возможности

- CRUD для пользователей, материалов и тегов
- Фильтрация материалов по статусу, типу, приоритету
- Связь материалов и тегов (многие-ко-многим)
- Асинхронный API (FastAPI)
- Миграции Alembic
- Seed-скрипт для тестовых данных
- Swagger UI (`/docs`)
- Линтинг и автоформатирование (ruff, black)
- Готово для CI/CD и Docker

---

## ⚡ Быстрый старт (локально)

```bash
# Клонируй репозиторий и перейди в папку проекта
git clone <repo-url>
cd 30bit

# Настрой виртуальное окружение
 uv venv .venv -p 3.12

# Настрои и отредактируй .env по необходимости
cp .env.example .env

# Установи зависимости
uv sync

# Применить миграции
uv run alembic upgrade head

# Заполнить тестовыми данными
uv run python scripts/seed_data.py

# Запустить приложение
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Открыть Swagger UI
http://localhost:8000/docs
```

---

## 🐳 Запуск в Docker

```bash
# Перейти в папку deployment
cd deployment

# Собрать и запустить сервисы (app + postgres)
# Миграции и seed-данные применяются автоматически
docker compose up --build

# Проверить развертывание
./check_deployment.sh

# API будет доступен на http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

**Примечание:** Все переменные окружения берутся из `deployment/.env.docker`. Для продакшена отредактируйте этот файл.

---

## 🧪 Тесты

```bash
# Запустить тесты
pytest
```

---

## 🛠️ Основные команды

- `uv run alembic upgrade head` — применить миграции
- `uv run python scripts/seed_data.py` — заполнить тестовыми данными
- `uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000` — запуск API
- `uv run ruff check .` — линтинг
- `uv run pytest` — тесты

---

## 📝 API

- Swagger UI: [`/docs`](http://localhost:8000/docs)
- Примеры запросов см. в документации

---

## 🗂️ Структура проекта

```
src/
  api/           # FastAPI роутеры
  application/   # Сервисы, схемы
  domain/        # Сущности, enums, exceptions
  infrastructure/# Репозитории, модели
  config.py      # Настройки
scripts/
  seed_data.py   # Заполнение тестовыми данными
alembic/         # Миграции
deployment/      # Docker, .env.docker
```

---

## 🏗️ CI/CD

- Линтинг и тесты через GitHub Actions (см. `.github/workflows/ci.yml`)
- Сборка Docker-образа

---

## 📄 Лицензия

MIT

---

## 👤 Автор

[Vasiliy](mailto:ogodevonline@gmail.com)