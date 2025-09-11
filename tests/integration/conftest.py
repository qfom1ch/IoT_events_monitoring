import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import test_settings
from src.infrastructure.di.container import create_container_test
from src.infrastructure.di.providers.mongo_providers import BeanieInitializer


@pytest_asyncio.fixture
async def container_test():
    container = create_container_test()

    await container.get(BeanieInitializer)

    client = await container.get(AsyncIOMotorClient)
    db = client[test_settings.DATABASE_NAME]

    collection_names = await db.list_collection_names()
    for collection_name in collection_names:
        await db[collection_name].delete_many({})

    async with container() as request_container:
        yield request_container

    client.close()
