#!/bin/bash

# Скрипт для проверки развертывания Reading List API
# Запускайте из папки deployment: ./check_deployment.sh

set -e

echo "🔍 Проверка развертывания Reading List API"
echo "=========================================="

# Проверка, что docker-compose запущен
if ! docker compose ps | grep -q "reading_list_api"; then
    echo "❌ Контейнер reading_list_api не найден. Запустите 'docker-compose up --build' сначала."
    exit 1
fi

echo "✅ Контейнеры запущены"

# Ожидание готовности API
echo "⏳ Ожидание готовности API..."
for i in {1..30}; do
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo "✅ API готов"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ API не отвечает после 30 секунд ожидания"
        exit 1
    fi
    sleep 1
done

# Проверка здоровья API
echo "🔍 Проверка здоровья API..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Эндпоинт здоровья работает"
else
    echo "⚠️  Эндпоинт здоровья не найден (возможно, не реализован)"
fi

# Проверка Swagger UI
echo "🔍 Проверка Swagger UI..."
if curl -s http://localhost:8000/docs | grep -q "swagger"; then
    echo "✅ Swagger UI доступен"
else
    echo "❌ Swagger UI не работает"
    exit 1
fi

# Проверка подключения к базе данных через API
echo "🔍 Проверка подключения к базе данных..."
# Попробуем получить список пользователей (должен вернуть пустой массив или данные)
if [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/api/v1/users)" = "200" ]; then
    echo "✅ API может подключиться к базе данных"
else
    echo "❌ Проблема с подключением к базе данных"
    exit 1
fi

# Проверка seed-данных
echo "🔍 Проверка наличия тестовых данных..."
user_count=$(curl -s http://localhost:8000/api/v1/users | jq '. | length' 2>/dev/null || echo "0")
if [ "$user_count" -gt 0 ]; then
    echo "✅ Найдено $user_count пользователей (seed-данные загружены)"
else
    echo "⚠️  Пользователи не найдены (seed-данные могут не загрузиться)"
fi

echo ""
echo "🎉 Развертывание успешно! API доступен на:"
echo "   🌐 http://localhost:8000"
echo "   📚 Swagger UI: http://localhost:8000/docs"
echo ""
echo "Для остановки: docker-compose down"
