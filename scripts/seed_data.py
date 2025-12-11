"""
Скрипт для заполнения базы тестовыми пользователями, тегами и материалами
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from datetime import datetime
from sqlalchemy import select

from src.database import AsyncSessionLocal, init_db
from src.infrastructure.models.item import ItemModel
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.tag_repository import TagRepository
from src.infrastructure.repositories.item_repository import ItemRepository
from src.domain.entities.user import User
from src.domain.entities.tag import Tag
from src.domain.entities.item import Item
from src.domain.enums import ItemKind, ItemStatus, Priority


async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        tag_repo = TagRepository(session)
        item_repo = ItemRepository(session)

        # Создаем пользователей
        now = datetime.now()
        users_data = [
            {"email": "alice@example.com", "display_name": "Alice"},
            {"email": "bob@example.com", "display_name": "Bob"},
        ]
        created_users = []
        for user_data in users_data:
            # Проверяем, есть ли пользователь
            existing = await user_repo.get_by_email(user_data["email"])
            if existing:
                created_users.append(existing)
            else:
                user = User(
                    id=None,
                    email=user_data["email"],
                    display_name=user_data["display_name"],
                    created_at=now,
                )
                created = await user_repo.create(user)
                created_users.append(created)

        # Создаем теги для Alice
        alice_id = created_users[0].id
        tags_data = ["python", "fastapi", "devops"]
        created_tags = []
        for tag_name in tags_data:
            existing_tag = await tag_repo.get_by_user_and_name(alice_id, tag_name)
            if existing_tag:
                created_tags.append(existing_tag)
            else:
                tag = Tag(id=None, user_id=alice_id, name=tag_name)
                created = await tag_repo.create(tag)
                created_tags.append(created)

        # Создаем материалы для Alice
        items_data = [
            {
                "title": "Clean Code",
                "kind": ItemKind.BOOK,
                "status": ItemStatus.PLANNED,
                "priority": Priority.HIGH,
                "notes": "Must read for software developers",
            },
            {
                "title": "FastAPI Tutorial",
                "kind": ItemKind.ARTICLE,
                "status": ItemStatus.READING,
                "priority": Priority.NORMAL,
                "notes": "Official docs",
            },
        ]
        created_items = []
        for item_data in items_data:
            # Проверяем, есть ли материал с таким названием у Alice
            stmt = await session.execute(
                select(ItemModel)
                .where(ItemModel.user_id == alice_id)
                .where(ItemModel.title == item_data["title"])
            )
            existing_item = stmt.scalar_one_or_none()
            if existing_item:
                created_items.append(await item_repo.to_entity(existing_item))
            else:
                item = Item(
                    id=None,
                    user_id=alice_id,
                    title=item_data["title"],
                    kind=item_data["kind"],
                    status=item_data["status"],
                    priority=item_data["priority"],
                    notes=item_data["notes"],
                    created_at=now,
                    updated_at=now,
                )
                created = await item_repo.create(item)
                created_items.append(created)

        # Привязываем теги к материалам (только если их еще нет)
        async def set_tags_if_needed(item, tag_ids):
            result = await item_repo.get_by_id_with_tags(item.id)
            current_tag_ids = set(result[1]) if result else set()
            new_tag_ids = set(tag_ids)
            if current_tag_ids != new_tag_ids:
                await item_repo.set_tags(item.id, list(new_tag_ids))

        await set_tags_if_needed(
            created_items[0], [created_tags[0].id, created_tags[2].id]
        )  # Clean Code: python, devops
        await set_tags_if_needed(
            created_items[1], [created_tags[1].id]
        )  # FastAPI Tutorial: fastapi

        await session.commit()
        print("Seed data inserted successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
