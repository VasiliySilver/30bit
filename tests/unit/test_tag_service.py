"""
Юнит-тесты для TagService
"""
import pytest
from src.application.schemas.tag import TagCreate
from src.domain.exceptions import DuplicateEntityError, EntityNotFoundError


@pytest.mark.asyncio
async def test_create_tag_success(tag_service, test_user):
    """Успешное создание тега"""
    data = TagCreate(name="python")
    tag = await tag_service.create_tag(test_user.id, data)
    
    assert tag.id is not None
    assert tag.name == "python"
    assert tag.user_id == test_user.id


@pytest.mark.asyncio
async def test_create_duplicate_tag(tag_service, test_user):
    """Попытка создать дубликат тега"""
    data = TagCreate(name="python")
    await tag_service.create_tag(test_user.id, data)
    
    with pytest.raises(DuplicateEntityError):
        await tag_service.create_tag(test_user.id, data)


@pytest.mark.asyncio
async def test_get_tag_success(tag_service, test_user):
    """Успешное получение тега по ID"""
    data = TagCreate(name="fastapi")
    created_tag = await tag_service.create_tag(test_user.id, data)
    
    tag = await tag_service.get_tag(created_tag.id, test_user.id)
    assert tag.id == created_tag.id
    assert tag.name == "fastapi"


@pytest.mark.asyncio
async def test_get_tag_not_found(tag_service, test_user):
    """Получение несуществующего тега"""
    with pytest.raises(EntityNotFoundError):
        await tag_service.get_tag(999, test_user.id)


@pytest.mark.asyncio
async def test_get_user_tags(tag_service, test_user):
    """Получение всех тегов пользователя"""
    await tag_service.create_tag(test_user.id, TagCreate(name="python"))
    await tag_service.create_tag(test_user.id, TagCreate(name="fastapi"))
    
    tags = await tag_service.get_user_tags(test_user.id)
    assert len(tags) == 2
    assert any(t.name == "python" for t in tags)
    assert any(t.name == "fastapi" for t in tags)


@pytest.mark.asyncio
async def test_delete_tag(tag_service, test_user):
    """Удаление тега"""
    data = TagCreate(name="pytest")
    tag = await tag_service.create_tag(test_user.id, data)
    
    result = await tag_service.delete_tag(tag.id, test_user.id)
    assert result is True
    
    with pytest.raises(EntityNotFoundError):
        await tag_service.get_tag(tag.id, test_user.id)