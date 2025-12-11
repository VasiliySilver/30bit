"""
Интеграционные тесты для Tags API
"""

import uuid


def test_create_tag(client):
    """Создание нового тега"""
    tag_name = f"test_tag_{uuid.uuid4().hex[:8]}"
    response = client.post("/api/v1/tags", json={"name": tag_name})
    assert response.status_code == 201
    tag = response.json()
    assert tag["name"] == tag_name.lower()  # name нормализуется
    assert tag["user_id"] == 1
    assert "id" in tag


def test_create_tag_duplicate(client):
    """Создание тега с дублирующимся именем"""
    tag_name = f"duplicate_tag_{uuid.uuid4().hex[:8]}"

    # Создаем первый тег
    response1 = client.post("/api/v1/tags", json={"name": tag_name})
    assert response1.status_code == 201

    # Пытаемся создать дубликат
    response2 = client.post("/api/v1/tags", json={"name": tag_name})
    assert response2.status_code == 409
    error = response2.json()
    assert error["detail"]["error"] == "DuplicateEntityError"


def test_get_tags(client):
    """Получение списка тегов пользователя"""
    # Создаем несколько тегов
    tag_names = [f"tag_{i}_{uuid.uuid4().hex[:4]}" for i in range(3)]
    created_tags = []

    for name in tag_names:
        response = client.post("/api/v1/tags", json={"name": name})
        assert response.status_code == 201
        created_tags.append(response.json())

    # Получаем список
    response = client.get("/api/v1/tags")
    assert response.status_code == 200
    tags = response.json()
    assert isinstance(tags, list)
    assert len(tags) >= 3

    # Проверяем, что наши теги в списке
    tag_names_lower = [name.lower() for name in tag_names]
    returned_names = [tag["name"] for tag in tags]
    for name in tag_names_lower:
        assert name in returned_names


def test_get_tag_by_id(client):
    """Получение тега по ID"""
    tag_name = f"get_test_{uuid.uuid4().hex[:8]}"

    # Создаем тег
    create_response = client.post("/api/v1/tags", json={"name": tag_name})
    assert create_response.status_code == 201
    created_tag = create_response.json()
    tag_id = created_tag["id"]

    # Получаем тег по ID
    response = client.get(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 200
    tag = response.json()
    assert tag["id"] == tag_id
    assert tag["name"] == tag_name.lower()
    assert tag["user_id"] == 1


def test_get_tag_not_found(client):
    """Получение несуществующего тега"""
    response = client.get("/api/v1/tags/99999")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["error"] == "EntityNotFoundError"


def test_delete_tag(client):
    """Удаление тега"""
    tag_name = f"delete_test_{uuid.uuid4().hex[:8]}"

    # Создаем тег
    create_response = client.post("/api/v1/tags", json={"name": tag_name})
    assert create_response.status_code == 201
    tag_id = create_response.json()["id"]

    # Удаляем тег
    delete_response = client.delete(f"/api/v1/tags/{tag_id}")
    assert delete_response.status_code == 200
    message = delete_response.json()
    assert message["message"] == "Тег успешно удален"

    # Проверяем, что тег удален
    get_response = client.get(f"/api/v1/tags/{tag_id}")
    assert get_response.status_code == 404


def test_delete_tag_not_found(client):
    """Удаление несуществующего тега"""
    response = client.delete("/api/v1/tags/99999")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["error"] == "EntityNotFoundError"
