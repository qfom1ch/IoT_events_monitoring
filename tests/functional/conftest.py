from collections.abc import AsyncGenerator
from typing import Any

import httpx
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import test_settings
from src.infrastructure.di.providers.mongo_providers import BeanieInitializer
from tests.functional.test_app import create_test_app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, Any]:
    app = create_test_app()
    await app.state.dishka_container.get(BeanieInitializer)

    client = await app.state.dishka_container.get(AsyncIOMotorClient)
    db = client[test_settings.DATABASE_NAME]

    collection_names = await db.list_collection_names()
    for collection_name in collection_names:
        await db[collection_name].delete_many({})

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client
