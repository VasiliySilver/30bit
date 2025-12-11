"""
Интеграционные тесты для Items API
"""

import pytest
import uuid


@pytest.fixture
def test_tags(client):
    """Создает тестовые теги"""
    tag1_resp = client.post(
        "/api/v1/tags", json={"name": f"python_{uuid.uuid4().hex[:4]}"}
    )
    assert tag1_resp.status_code == 201
    tag1 = tag1_resp.json()
    print(f"Tag1: {tag1}")

    tag2_resp = client.post(
        "/api/v1/tags", json={"name": f"fastapi_{uuid.uuid4().hex[:4]}"}
    )
    assert tag2_resp.status_code == 201
    tag2 = tag2_resp.json()
    print(f"Tag2: {tag2}")

    return [tag1["id"], tag2["id"]]


def test_create_item(client):
    """Создание материала"""
    response = client.post(
        "/api/v1/items",
        json={
            "title": "Clean Code",
            "kind": "book",
            "status": "planned",
            "priority": "high",
            "notes": "Must read",
            "tag_ids": [],
        },
    )
    # Выводим ошибку для отладки
    if response.status_code != 201:
        print(f"Response: {response.text}")
    assert response.status_code == 201, f"Failed to create item: {response.text}"
    item = response.json()
    assert item["title"] == "Clean Code"
    assert item["kind"] == "book"


def test_create_item_with_tags(client, test_tags):
    """Создание материала с тегами"""
    print(f"Test tags: {test_tags}")
    response = client.post(
        "/api/v1/items",
        json={
            "title": "FastAPI Tutorial",
            "kind": "article",
            "status": "reading",
            "priority": "normal",
            "notes": "Official docs",
            "tag_ids": test_tags,
        },
    )
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")
    assert response.status_code == 201
    item = response.json()
    assert item["title"] == "FastAPI Tutorial"
    assert len(item["tag_ids"]) == 2


def test_get_items(client):
    """Получение списка материалов"""
    # Создаем материалы
    client.post(
        "/api/v1/items",
        json={
            "title": "Item 1",
            "kind": "book",
            "status": "planned",
            "priority": "high",
            "notes": None,
            "tag_ids": [],
        },
    )
    client.post(
        "/api/v1/items",
        json={
            "title": "Item 2",
            "kind": "article",
            "status": "reading",
            "priority": "normal",
            "notes": None,
            "tag_ids": [],
        },
    )

    response = client.get("/api/v1/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2


def test_get_item_by_id(client):
    """Получение материала по ID"""
    create_response = client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "kind": "book",
            "status": "planned",
            "priority": "normal",
            "notes": None,
            "tag_ids": [],
        },
    )
    item_id = create_response.json()["id"]

    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == item_id
    assert item["title"] == "Test Item"


def test_update_item(client):
    """Обновление материала"""
    create_response = client.post(
        "/api/v1/items",
        json={
            "title": "Old Title",
            "kind": "book",
            "status": "planned",
            "priority": "normal",
            "notes": None,
            "tag_ids": [],
        },
    )
    item_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/items/{item_id}", json={"title": "New Title", "status": "reading"}
    )
    assert response.status_code == 200
    item = response.json()
    assert item["title"] == "New Title"
    assert item["status"] == "reading"


def test_delete_item(client):
    """Удаление материала"""
    create_response = client.post(
        "/api/v1/items",
        json={
            "title": "Item to Delete",
            "kind": "article",
            "status": "planned",
            "priority": "low",
            "notes": None,
            "tag_ids": [],
        },
    )
    item_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200

    # Проверяем, что удален
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404


def test_filter_items_by_kind(client):
    """Фильтрация материалов по типу"""
    client.post(
        "/api/v1/items",
        json={
            "title": "Book 1",
            "kind": "book",
            "status": "planned",
            "priority": "high",
            "notes": None,
            "tag_ids": [],
        },
    )
    client.post(
        "/api/v1/items",
        json={
            "title": "Article 1",
            "kind": "article",
            "status": "reading",
            "priority": "normal",
            "notes": None,
            "tag_ids": [],
        },
    )

    response = client.get("/api/v1/items?kind=book")
    assert response.status_code == 200
    items = response.json()
    assert all(item["kind"] == "book" for item in items)


def test_filter_items_by_status(client):
    """Фильтрация материалов по статусу"""
    client.post(
        "/api/v1/items",
        json={
            "title": "Book 1",
            "kind": "book",
            "status": "planned",
            "priority": "high",
            "notes": None,
            "tag_ids": [],
        },
    )
    client.post(
        "/api/v1/items",
        json={
            "title": "Article 1",
            "kind": "article",
            "status": "reading",
            "priority": "normal",
            "notes": None,
            "tag_ids": [],
        },
    )

    response = client.get("/api/v1/items?status=reading")
    assert response.status_code == 200
    items = response.json()
    assert all(item["status"] == "reading" for item in items)


def test_filter_items_by_priority(client):
    """Фильтрация материалов по приоритету"""
    client.post(
        "/api/v1/items",
        json={
            "title": "High Priority",
            "kind": "book",
            "status": "planned",
            "priority": "high",
            "notes": None,
            "tag_ids": [],
        },
    )
    client.post(
        "/api/v1/items",
        json={
            "title": "Low Priority",
            "kind": "article",
            "status": "reading",
            "priority": "low",
            "notes": None,
            "tag_ids": [],
        },
    )

    response = client.get("/api/v1/items?priority=high")
    assert response.status_code == 200
    items = response.json()
    assert all(item["priority"] == "high" for item in items)
