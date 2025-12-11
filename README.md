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

# Установи зависимости
uv pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Заполнить тестовыми данными
PYTHONPATH=. uv run python scripts/seed_data.py

# Запустить приложение
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Открыть Swagger UI
http://localhost:8000/docs
```

---

## 🐳 Запуск в Docker

```bash
# Собрать и запустить сервисы (app + postgres)
docker-compose up --build

# Применить миграции внутри контейнера
docker-compose exec app alembic upgrade head

# Заполнить тестовыми данными
docker-compose exec app python scripts/seed_data.py
```

---

## 🧪 Тесты

```bash
# Запустить тесты
pytest
```

---

## 🛠️ Основные команды

- `alembic upgrade head` — применить миграции
- `PYTHONPATH=. python scripts/seed_data.py` — заполнить тестовыми данными
- `uv run uvicorn src.main:app --reload` — запуск API
- `ruff check .` — линтинг
- `pytest` — тесты

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