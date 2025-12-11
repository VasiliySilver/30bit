"""
Юнит-тесты для ItemService
"""

import pytest

from src.application.schemas.item import ItemCreate, ItemUpdate
from src.application.schemas.tag import TagCreate
from src.domain.enums import ItemKind, ItemStatus, Priority
from src.domain.exceptions import EntityNotFoundError


@pytest.mark.asyncio
async def test_create_item_success(item_service, test_user):
    """Успешное создание материала"""
    data = ItemCreate(
        title="Clean Code",
        kind=ItemKind.BOOK,
        status=ItemStatus.PLANNED,
        priority=Priority.HIGH,
        notes="Must read",
        tag_ids=[],
    )
    item = await item_service.create_item(test_user.id, data)

    assert item.id is not None
    assert item.title == "Clean Code"
    assert item.kind == ItemKind.BOOK
    assert item.user_id == test_user.id


@pytest.mark.asyncio
async def test_create_item_with_tags(item_service, tag_service, test_user):
    """Создание материала с тегами"""
    tag1 = await tag_service.create_tag(test_user.id, TagCreate(name="python"))
    tag2 = await tag_service.create_tag(test_user.id, TagCreate(name="fastapi"))

    data = ItemCreate(
        title="FastAPI Tutorial",
        kind=ItemKind.ARTICLE,
        status=ItemStatus.READING,
        priority=Priority.NORMAL,
        notes="Official docs",
        tag_ids=[tag1.id, tag2.id],
    )
    item = await item_service.create_item(test_user.id, data)

    assert item.id is not None
    assert len(item.tag_ids) == 2
    assert tag1.id in item.tag_ids
    assert tag2.id in item.tag_ids


@pytest.mark.asyncio
async def test_get_item(item_service, test_user):
    """Получение материала по ID"""
    data = ItemCreate(
        title="Test Item",
        kind=ItemKind.BOOK,
        status=ItemStatus.PLANNED,
        priority=Priority.NORMAL,
        notes=None,
        tag_ids=[],
    )
    created_item = await item_service.create_item(test_user.id, data)

    item = await item_service.get_item(created_item.id, test_user.id)
    assert item.id == created_item.id
    assert item.title == "Test Item"


@pytest.mark.asyncio
async def test_update_item(item_service, test_user):
    """Обновление материала"""
    data = ItemCreate(
        title="Old Title",
        kind=ItemKind.BOOK,
        status=ItemStatus.PLANNED,
        priority=Priority.NORMAL,
        notes=None,
        tag_ids=[],
    )
    item = await item_service.create_item(test_user.id, data)

    update_data = ItemUpdate(
        title="New Title",
        status=ItemStatus.READING,
        kind=item.kind,
        priority=item.priority,
        notes=item.notes,
        tag_ids=item.tag_ids,
    )
    updated = await item_service.update_item(item.id, test_user.id, update_data)

    assert updated.title == "New Title"
    assert updated.status == ItemStatus.READING


@pytest.mark.asyncio
async def test_delete_item(item_service, test_user):
    """Удаление материала"""
    data = ItemCreate(
        title="Item to Delete",
        kind=ItemKind.ARTICLE,
        status=ItemStatus.PLANNED,
        priority=Priority.LOW,
        notes=None,
        tag_ids=[],
    )
    item = await item_service.create_item(test_user.id, data)

    result = await item_service.delete_item(item.id, test_user.id)
    assert result is True

    with pytest.raises(EntityNotFoundError):
        await item_service.get_item(item.id, test_user.id)


@pytest.mark.asyncio
async def test_filter_items_by_kind(item_service, test_user):
    """Фильтрация материалов по типу"""
    await item_service.create_item(
        test_user.id,
        ItemCreate(
            title="Book 1",
            kind=ItemKind.BOOK,
            status=ItemStatus.PLANNED,
            priority=Priority.HIGH,
            notes=None,
            tag_ids=[],
        ),
    )
    await item_service.create_item(
        test_user.id,
        ItemCreate(
            title="Article 1",
            kind=ItemKind.ARTICLE,
            status=ItemStatus.READING,
            priority=Priority.NORMAL,
            notes=None,
            tag_ids=[],
        ),
    )

    books = await item_service.get_user_items(test_user.id, kind=ItemKind.BOOK)
    assert len(books) == 1
    assert books[0].kind == ItemKind.BOOK


@pytest.mark.asyncio
async def test_filter_items_by_status(item_service, test_user):
    """Фильтрация материалов по статусу"""
    await item_service.create_item(
        test_user.id,
        ItemCreate(
            title="Book 1",
            kind=ItemKind.BOOK,
            status=ItemStatus.PLANNED,
            priority=Priority.HIGH,
            notes=None,
            tag_ids=[],
        ),
    )
    await item_service.create_item(
        test_user.id,
        ItemCreate(
            title="Article 1",
            kind=ItemKind.ARTICLE,
            status=ItemStatus.READING,
            priority=Priority.NORMAL,
            notes=None,
            tag_ids=[],
        ),
    )

    reading = await item_service.get_user_items(test_user.id, status=ItemStatus.READING)
    assert len(reading) == 1
    assert reading[0].status == ItemStatus.READING
