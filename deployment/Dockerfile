# Dockerfile для Reading List API

FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директорию для данных
RUN mkdir -p /app/data

# Экспонируем порт
EXPOSE 8000

# Команда запуска (через uvicorn)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
